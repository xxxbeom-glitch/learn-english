"""시즌 1 Part 1 여섯 화를 조립한다. 시험판 코드다.

season_manifest.py가 만든 묶음과 일레븐랩스 단어 시간(cuts.json)으로
인물별 음성을 줄 단위로 잘라 화 순서로 붙이고, 화마다 mp3와 시간표를 만든다.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from season_manifest import STORY, plain, rows, sections

HERE = Path(__file__).parent
SEASON = HERE / "audio" / "season"
RAW = HERE / "audio" / "raw"
TMP = SEASON / "tmp"
SR = 44100
LINE_GAP = 0.35
SPEAK_PAUSE = 3.0
PAD = 0.03


def run(*args):
    subprocess.run(args, check=True, capture_output=True)


def ff(*args):
    return subprocess.run(["ffmpeg", "-hide_banner", *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stderr


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                check=True, capture_output=True, text=True).stdout)


def silences(path):
    out = ff("-i", str(path), "-af", "silencedetect=noise=-40dB:d=0.12", "-f", "null", "-")
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
    return list(zip(starts, ends))


def loudness(path):
    out = ff("-i", str(path), "-af", "ebur128=framelog=quiet", "-f", "null", "-")
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", out)[-1])


class Source:
    """인물 음성 파일 하나. 줄 사이 침묵의 가운데를 경계로 삼아 웃음과 한숨이 잘리지 않게 한다."""

    def __init__(self, name, cuts):
        self.path = SEASON / f"{name}.mp3"
        self.total = duration(self.path)
        self.gain = -18 - loudness(self.path)
        sil = silences(self.path)
        bounds = [0.0]
        for a, b in zip(cuts, cuts[1:]):
            lo, hi = a["end"], b["start"]
            # 받아쓰기의 끝 시각은 다음 줄 시작까지 늘어날 때가 있다. 그래서 끝 시각 대신
            # 다음 줄이 시작하기 바로 전의 침묵을 경계로 쓴다. (2026-11-08 7화 예시 끝에 다음 줄 앞이 붙던 문제)
            near = [s for s in sil if a["start"] < s[1] <= hi + 0.15]
            best = max(near, key=lambda s: s[1]) if near else (lo, hi)
            bounds.append((best[0] + best[1]) / 2)
        bounds.append(self.total)
        self.clips = {}
        self.order = []
        for i, c in enumerate(cuts):
            lo, hi = bounds[i], bounds[i + 1]
            for s in sil:
                if s[0] <= lo < s[1]:
                    lo = s[1]
                if s[0] < hi <= s[1]:
                    hi = s[0]
            clip = {"start": max(0, lo - PAD), "end": min(self.total, hi + PAD), "cut": c}
            self.clips.setdefault(c["key"], clip)
            self.order.append(clip)


class Builder:
    def __init__(self, n):
        self.n, self.parts, self.t, self.lines, self.sections = n, [], 0.0, [], []
        self.dir = TMP / f"ep{n}"
        self.dir.mkdir(parents=True, exist_ok=True)

    def _add(self, path):
        self.parts.append(path)
        self.t += duration(path)

    def silence(self, seconds):
        p = self.dir / f"s{len(self.parts):03d}.wav"
        run("ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{seconds}", "-c:a", "pcm_s16le", str(p))
        self._add(p)

    def sfx(self, name):
        p = self.dir / f"x{len(self.parts):03d}.wav"
        run("ffmpeg", "-y", "-i", str(RAW / name), "-af", "volume=-9dB", "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(p))
        self._add(p)

    def clip(self, src, c):
        p = self.dir / f"c{len(self.parts):03d}.wav"
        run("ffmpeg", "-y", "-i", str(src.path), "-ss", f"{c['start']}", "-to", f"{c['end']}",
            "-af", f"volume={src.gain:.2f}dB,afade=t=in:d=0.01,areverse,afade=t=in:d=0.02,areverse",
            "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(p))
        self._add(p)

    def line(self, section, who, src, c, text, meaning, kind="line"):
        begin = self.t
        self.clip(src, c)
        self.lines.append({"section": section, "speaker": who, "text": text, "meaning": meaning, "kind": kind,
                           "start": round(begin, 2), "end": round(self.t, 2)})

    def narrate(self, section, src, c, kind="line"):
        """해설자 한 묶음을 문장별 자막으로 나눈다. 소리는 이어서 붙인다."""
        begin = self.t
        self.clip(src, c)
        sents = split_sentences(c["cut"]["words"])
        for i, (text, start) in enumerate(sents):
            a = begin if i == 0 else begin + start - c["start"]
            b = self.t if i == len(sents) - 1 else begin + sents[i + 1][1] - c["start"]
            self.lines.append({"section": section, "speaker": "해설자", "text": text, "meaning": None, "kind": kind,
                               "start": round(a, 2), "end": round(b, 2)})

    def section(self, key, title):
        self.sections.append({"key": key, "title": title, "start": round(self.t, 2)})


def split_sentences(words):
    out, cur, start = [], [], None
    for i, w in enumerate(words):
        if start is None:
            start = w["start"]
        cur.append(w["text"])
        nxt = words[i + 1]["text"] if i + 1 < len(words) else ""
        if re.search(r"[.!?]$", w["text"]) and not (nxt.startswith(("라는", "는", "인데")) or nxt == "가"):
            out.append((" ".join(cur), start))
            cur, start = [], None
    if cur:
        out.append((" ".join(cur), start))
    return out


def meanings(sec):
    """화면 해설의 문장과 응용에서 영어 뜻을 모은다."""
    out = {}
    for l in sec["E"].split("\n"):
        l = re.sub(r"^\s*(- )?(응용: )?", "", l)
        parts = [p.strip() for p in l.split(" || ")]
        if len(parts) >= 2 and parts[0] and not l.startswith("주의"):
            out[parts[0]] = parts[1]
    return out


def main():
    cuts = json.loads((SEASON / "cuts.json").read_text(encoding="utf-8"))
    words = json.loads((SEASON / "words.json").read_text(encoding="utf-8"))
    for name, rows_ in cuts.items():
        for c, w in zip(rows_, words[name]):
            c["words"] = w
    text = STORY.read_text(encoding="utf-8")
    only = {int(x) for x in sys.argv[1:]}
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        n = int(block.split("화")[0])
        if only and n not in only:
            continue
        sec = sections(block)
        src = {name.split("-", 1)[1]: Source(name, c) for name, c in cuts.items() if name.startswith(f"ep{n}-")}

        def pick(who, key):
            """나중에 추가로 만든 문장은 '인물2', '인물3' 파일에 있다. 가장 최근 파일을 먼저 찾는다."""
            for name in (who + "3", who + "2", who):
                if name in src and key in src[name].clips:
                    return src[name], src[name].clips[key]
            raise KeyError((who, key))

        mean = meanings(sec)
        replay = [l.split(": ", 1)[1].split(" || ") for l in sec["D"].split("\n") if " || " in l]
        b = Builder(n)
        b.sfx("sfx-start.mp3")
        b.silence(0.3)

        def dialogue(section, ko):
            for i, (who, raw) in enumerate(rows(sec["A"])):
                if i:
                    b.silence(LINE_GAP)
                key = plain(raw)
                b.line(section, who, *pick(who, key), key, ko[i][1] if ko else None)

        b.section("dialogue", "대화")
        dialogue("dialogue", None)
        b.silence(0.8)

        b.section("commentary", "해설")
        for i, (who, raw) in enumerate(rows(sec["B"])):
            if i:
                b.silence(LINE_GAP)
            if who == "해설자":
                b.narrate("commentary", *pick(who, plain(raw)))
            else:
                key = plain(raw)
                b.line("commentary", who, *pick(who, key), key, mean.get(key))
        b.silence(0.7)

        b.section("practice", "말해보기")
        pr = rows(sec["C"])
        for i in range(0, len(pr) - 1, 2):
            ko = plain(pr[i][1])
            b.narrate("practice", *pick("해설자", ko), kind="prompt")
            start = b.t
            b.silence(SPEAK_PAUSE)
            b.lines.append({"section": "practice", "speaker": "나", "text": "직접 말해보세요", "meaning": None,
                            "kind": "pause", "start": round(start, 2), "end": round(b.t, 2)})
            who, key = pr[i + 1][0], plain(pr[i + 1][1])
            b.line("practice", who, *pick(who, key), key, ko, kind="answer")
            b.silence(0.5)
        b.narrate("practice", *pick("해설자", plain(pr[-1][1])))
        b.silence(0.7)

        b.section("replay", "대화 다시 듣기")
        dialogue("replay", replay)
        b.silence(0.5)
        b.sfx("sfx-end.mp3")

        out = SEASON / f"s1-{n:02d}.mp3"
        listing = b.dir / "list.txt"
        listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in b.parts), encoding="utf-8")
        run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-ar", str(SR), "-ac", "1", "-c:a", "libmp3lame", "-b:a", "128k", str(out))
        (SEASON / f"s1-{n:02d}.json").write_text(json.dumps(
            {"duration": round(b.t, 2), "sections": b.sections, "lines": b.lines}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(n, f"{b.t:.1f}초", len(b.lines), out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
