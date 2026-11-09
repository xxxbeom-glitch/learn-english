"""팟캐스트 앨범 트랙을 앱에 넣을 준비를 한다. 버리는 코드다.

구간 이름은 talk다. 수업 대화(dialogue)는 한글 뜻을 숨기지만, 팟캐스트는 줄마다 한글 뜻을 보인다.
대본(content/podcasts/album-NN-part-N.md)의 줄과 차례별 음성 조각의 길이로 시간표를 만들고,
이어 붙인 트랙(MP3)을 앱용 Opus 24kbps(webm)로 바꾼다.
조각은 stitch.sh와 같이 줄마다 뒤에 0.35초를 띄워 이었으므로, 시간표도 같은 규칙으로 계산한다.

사용: python build_podcast.py <조각 폴더 상위> <트랙 MP3 폴더> [앨범 번호, 기본 1]
  조각 폴더 상위 아래에 p1/, p2/ ... 가 있고 그 안에 01.mp3, 02.mp3 ... 가 있다.
  트랙 MP3 폴더에는 album-01-part-1.mp3 ... 가 있다.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
CONTENT = HERE.parent.parent / "content" / "podcasts"
OUT = HERE / "audio" / "podcast"
APP = HERE / "app"
GAP = 0.35
ALBUM = 1


def parse(md):
    """'**Mike:** [tag] text' 다음 줄 '> 한글 뜻'을 한 쌍으로 읽는다. 대괄호 표시는 화면에 보이지 않는다."""
    title = re.search(r"^# .*Part \d+: (.+)$", md, re.M).group(1).strip()
    lines, rows = [], md.split("\n---\n")[1].strip().split("\n")
    for i, raw in enumerate(rows):
        m = re.match(r"\*\*(\w+):\*\* (.+)", raw.strip())
        if not m:
            continue
        ko = next((r.strip()[2:].strip() for r in rows[i + 1:i + 3] if r.strip().startswith("> ")), None)
        text = re.sub(r"\[[^\]]*\]\s*", "", m.group(2)).strip()
        lines.append({"speaker": m.group(1), "text": text, "meaning": ko})
    return title, lines


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]))


def silences(f):
    """조각 안에서 쉬는 틈(가운데 시각, 길이)을 찾는다."""
    err = subprocess.run(["ffmpeg", "-v", "info", "-i", str(f), "-af", "silencedetect=n=-35dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    en = [(float(a), float(b)) for a, b in re.findall(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", err)]
    return [((s + e) / 2, d) for s, (e, d) in zip(st, en)]


def split(f, d, group):
    """같은 사람이 이어 말한 줄은 한 조각으로 만들었다. 글자 수 비율로 어림한 자리에 가장 가까운 긴 틈에서 나눈다."""
    if len(group) == 1:
        return [(0.0, d)]
    gaps = [g for g in silences(f) if 0.3 < g[0] < d - 0.3]
    total = sum(len(l["text"]) for l in group)
    cuts, acc = [], 0
    for l in group[:-1]:
        acc += len(l["text"])
        guess = d * acc / total
        best = min(gaps, key=lambda g: abs(g[0] - guess) - g[1]) if gaps else (guess, 0)
        cuts.append(best[0])
        gaps = [g for g in gaps if g[0] > best[0]]
    edges = [0.0] + cuts + [d]
    return list(zip(edges[:-1], edges[1:]))


def main(clips, tracks, album=1):
    global ALBUM
    ALBUM = int(album)
    OUT.mkdir(parents=True, exist_ok=True)
    part = 0
    while (CONTENT / f"album-{ALBUM:02d}-part-{part + 1}.md").exists():
        part += 1
        title, lines = parse((CONTENT / f"album-{ALBUM:02d}-part-{part}.md").read_text(encoding="utf-8"))
        parts = sorted((Path(clips) / f"p{part}").glob("*.mp3"))
        if len(parts) == len(lines):
            # 한 사람 방송(앨범 3)은 줄마다 조각을 따로 만들었다.
            groups = [[l] for l in lines]
        else:
            groups = []
            for l in lines:
                if groups and groups[-1][-1]["speaker"] == l["speaker"]:
                    groups[-1].append(l)
                else:
                    groups.append([l])
        assert len(parts) == len(groups), (part, len(parts), len(groups))
        t, out = 0.0, []
        for group, f in zip(groups, parts):
            d = dur(f)
            for l, (a, b) in zip(group, split(f, d, group)):
                out.append(dict(l, section="talk", kind="line", start=round(t + a, 2), end=round(t + b, 2)))
            t += d + GAP
        src = Path(tracks) / f"album-{ALBUM:02d}-part-{part}.mp3"
        name = f"r{ALBUM}-{part:02d}"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-ac", "1", "-c:a", "libopus", "-b:a", "24k",
                        str(APP / f"{name}.webm")], check=True)
        total = dur(APP / f"{name}.webm")
        tl = {"title": title, "duration": round(total, 2),
              "sections": [{"key": "talk", "title": "대화", "start": 0}], "lines": out}
        (OUT / f"{name}.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
        print(name, title, len(out), "lines, timeline", round(t, 2), "track", round(total, 2))


if __name__ == "__main__":
    main(*sys.argv[1:4])
