"""쉐도잉 트랙 만들기: 소리를 이어 붙이고, 가사 화면용 시간표(timeline.json)를 함께 만든다.

python build_shadowing.py small-talk 1

대본: content/stories/shadowing-<album>.md 의 '## N. 제목' 아래 'A: 영어 ★' / '뜻: 한국어' 줄.
목소리: audio/shadowing/<album>/epNN/clips/d1..dN.mp3 (대본 줄 순서), g1(Now, repeat after me.), g2(One more time.).
흐름(2026-11-10 성범 결정): 시작음 → 대화 → Now, repeat after me. → 핵심 줄(★)마다 듣기, 멈춤, 듣기, 멈춤, 클릭음
(마지막 줄 뒤엔 클릭음 없음) → One more time. → 대화로 끝난다. 끝음은 없다.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
RAW = HERE / "audio" / "raw"
SR = 44100
# 앨범 폴더 이름 → 앱 파일 앞머리. 새 앨범은 뒤에 붙인다
TAG = {"small-talk": "s1", "daily-routine": "s2", "about-me": "s3", "social-skills": "s4", "eating-out": "s5", "speak-up": "s6", "swearing": "s7"}
GUIDE = {"g1": ("Now, repeat after me.", "이제 따라 말해 보세요."), "g2": ("One more time.", "한 번 더 들어 볼게요.")}


def script(album, n):
    text = (ROOT / "content" / "stories" / f"shadowing-{album}.md").read_text(encoding="utf-8")
    block = re.split(r"^## ", text, flags=re.M)
    block = next(b for b in block if re.match(rf"{n}\. ", b))
    title = re.match(r"\d+\. (.+)", block).group(1).strip()
    lines = []
    for raw in block.split("\n"):
        m = re.match(r"([AB]): (.+)", raw.strip())
        if m:
            en = m.group(2).strip()
            lines.append({"who": m.group(1), "text": en.replace("★", "").strip(), "key": "★" in en, "ko": None})
        m = re.match(r"뜻: (.+)", raw.strip())
        if m and lines:
            lines[-1]["ko"] = m.group(1).strip()
    return title, lines


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]))


def wav(src, af, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", af, "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(out)], check=True)


def silence(sec, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{sec:.3f}", "-c:a", "pcm_s16le", str(out)], check=True)


def build(album, n):
    d = HERE / "audio" / "shadowing" / album / f"ep{n:02d}"
    tmp = d / "tmp"; tmp.mkdir(exist_ok=True)
    title, lines = script(album, n)
    wav(RAW / "sfx-start-shadowing.mp3", "volume=-4dB", tmp / "start.wav")
    wav(RAW / "sfx-next-soft.mp3", "atrim=0:1.0,afade=t=out:st=0.9:d=0.1,volume=-4dB", tmp / "click.wav")
    for k in range(1, len(lines) + 1):
        wav(d / "clips" / f"d{k}.mp3", "anull", tmp / f"d{k}.wav")
    for g in GUIDE:
        wav(d / "clips" / f"{g}.mp3", "anull", tmp / f"{g}.wav")

    parts, tl, t = [], [], 0.0
    sil = {}

    def gap(sec):
        nonlocal t
        key = f"{sec:.2f}"
        if key not in sil:
            sil[key] = tmp / f"s_{key}.wav"; silence(sec, sil[key])
        parts.append(sil[key]); t += dur(sil[key])

    def put(f, line=None):
        nonlocal t
        L = dur(f); parts.append(f)
        if line:
            tl.append(line | {"start": round(t, 2), "end": round(t + L, 2)})
        t += L
        return L

    def say(k, section, kind="line"):
        l = lines[k - 1]
        speaker = "Me" if l["who"] == "A" else "Partner"
        return put(tmp / f"d{k}.wav", {"speaker": speaker, "text": l["text"], "meaning": l["ko"], "section": section, "kind": kind})

    def dialogue(section):
        for k in range(1, len(lines) + 1):
            if k > 1: gap(0.4)
            say(k, section)

    def guide(g, section):
        en, ko = GUIDE[g]
        put(tmp / f"{g}.wav", {"speaker": "Guide", "text": en, "meaning": ko, "section": section, "kind": "guide"})

    put(tmp / "start.wav"); gap(0.5)
    dialogue("talk"); gap(1.0)
    guide("g1", "repeat"); gap(0.6)
    keys = [k for k, l in enumerate(lines, 1) if l["key"]]
    for j, k in enumerate(keys):
        L = say(k, "repeat")
        p = round(L * 1.2 + 0.5, 2)
        tl.append({"kind": "pause", "section": "repeat", "start": round(t, 2), "end": round(t + p, 2)}); gap(p)
        say(k, "repeat", "again")
        tl.append({"kind": "pause", "section": "repeat", "start": round(t, 2), "end": round(t + p, 2)}); gap(p)
        if j < len(keys) - 1:
            put(tmp / "click.wav"); gap(0.6)
    guide("g2", "replay"); gap(0.6)
    dialogue("replay")

    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    name = f"{TAG[album]}-{n:02d}"
    mp3 = d / f"shadowing-{album}-{n:02d}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar", str(SR), "-ac", "1", "-c:a", "libmp3lame", "-b:a", "128k", str(mp3)], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-c:a", "libopus", "-b:a", "24k", "-ac", "1", str(d / f"{name}.webm")], check=True)
    out = {"title": title, "duration": round(dur(mp3), 2),
           "sections": [{"key": "talk", "title": "Listen", "start": 0}, {"key": "repeat", "title": "Repeat", "start": 0}, {"key": "replay", "title": "Listen again", "start": 0}],
           "lines": tl}
    (d / "timeline.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(name, out["duration"], len(tl))


if __name__ == "__main__":
    build(sys.argv[1], int(sys.argv[2]))
