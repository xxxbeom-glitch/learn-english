"""단어 오디오북(Words) 음성 (2026-11-10 성범 요청). 대본은 content/stories/words-NN.md.

python build_words.py clips 1   조각 목록(audio/words/ep01/clips.json). 같은 목소리의 같은 말은 한 번만 만든다.
python build_words.py build 1   조각(audio/words/ep01/clips/<id>.mp3)을 이어 붙여 w1-01.mp3와 timeline.json을 만든다.

한 단어: 단어 → 뜻(해설자) → 예문 → 단어 세 번(불규칙 과거형이면 두 꼴). 끝에 복습: 한국어 뜻 → 2초 멈춤 → 영어 단어.
단어를 한 번 더 들려줄 때와 복습 답은 처음 만든 단어 조각을 다시 쓴다. 소리는 모두 일레븐랩스, 시작음은 sfx-start-words.mp3, 단어 시작 클릭음은 sfx-word-click.mp3, 끝음과 복습 클릭음은 초급 것.
2026-11-10 성범 요청으로 1화를 앱의 Words 선반에 넣었다(build_page.py가 맨 뒤에 붙인다).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from beginner_v2 import VOICE, dur

HERE = Path(__file__).parent
STORIES = HERE.parent.parent / "content" / "stories"
OUT = HERE / "audio" / "words"
RAW = HERE / "audio" / "raw"
SR = 44100
GAP, WORD_GAP, PAUSE = 0.4, 2.0, 2.0  # 단어 사이 1.0 → 2.0초 (2026-11-10 성범: 다음 단어로 넘어가는 텀이 너무 짧다)
REPEAT, REPEAT_GAP = 3, 1.2
# 일레븐랩스가 만든 조각 맨 앞에 목소리가 아닌 '삑' 음이 붙은 것은 그만큼 잘라 낸다(초). 2026-11-10 성범: wake up 앞 '삑'
SKIP = {"e03": 0.155}  # 예문 뒤 단어를 세 번 들려준다 (2026-11-10 성범 요청, 옛: 한 번). 사이 0.6 → 1.2초 (성범: 너무 빨리 말하는 기계 같다)


def script(n):
    text = (STORIES / f"words-{n:02d}.md").read_text(encoding="utf-8")
    body = text.split(f"## {n}화 ", 1)[1]
    title = body.split("\n", 1)[0].strip()
    sec = dict(re.findall(r"^### (\S+)\n(.*?)(?=^### |\Z)", body, flags=re.M | re.S))
    words = []
    for row in sec["단어"].strip().splitlines():
        f = [x.strip() for x in row.split("|")]
        words.append({"word": f[0], "wv": f[1], "ko": f[2], "note": f[3], "ev": f[4],
                      "ex": f[5], "exko": f[7], "last": f[8] or f[0]})
    return {"n": n, "title": title, "intro": sec["도입"].strip(), "review": sec["복습"].strip(),
            "outro": sec["끝인사"].strip(), "words": words}


def steps(s):
    """(구간, 화자, 글, 뜻, 종류) 순서. 종류: line, word, prompt, pause, answer."""
    yield "intro", "해설자", s["intro"], None, "line"
    for w in s["words"]:
        # 단어 아래 뜻은 보이지 않는다. 바로 다음 해설이 뜻을 말한다 (2026-11-10 성범 요청). 앱 가사에는 line으로 적는다
        yield "words", w["wv"], w["word"], None, "word"
        yield "words", "해설자", w["note"], None, "line"
        # 예문 뜻은 가사 아래 글씨가 아니라 해설자가 소리로 읽는다 (2026-11-10 성범 요청)
        yield "words", w["ev"], w["ex"], None, "line"
        yield "words", "해설자", w["exko"], None, "line"
        yield "words", w["wv"], w["last"], None, "repeat"
    yield "review", "해설자", s["review"], None, "line"
    for w in s["words"]:
        yield "review", "해설자", w["ko"], None, "prompt"
        yield "review", None, None, None, "pause"
        yield "review", w["wv"], w["word"], None, "answer"  # 한국어 문제를 먼저 들려주므로 뜻은 붙이지 않는다
    yield "outro", "해설자", s["outro"], None, "line"


def ids(s):
    """(화자, 글) → 조각 id. 같은 화자의 같은 글은 한 조각이다.
    이미 만든 조각(clips.json)의 번호는 그대로 두고, 새 줄만 뒤 번호를 받는다(대본에 줄을 끼워도 옛 조각 파일이 어긋나지 않게)."""
    f = OUT / f"ep{s['n']:02d}" / "clips.json"
    m = {(c["who"], c["say"].split(" ", 1)[1]): c["id"] for c in json.loads(f.read_text(encoding="utf-8"))} if f.exists() else {}
    for _, who, text, _, kind in steps(s):
        if kind == "pause" or (who, text) in m:
            continue
        p = "n" if who == "해설자" else "e"
        m[(who, text)] = f"{p}{sum(v.startswith(p) for v in m.values()) + 1:02d}"
    return m


def clips(n):
    s = script(n)
    out = [{"id": cid, "who": who, "voice": VOICE[who], "say": f"[casual] {text}"} for (who, text), cid in ids(s).items()]
    d = OUT / f"ep{n:02d}"
    (d / "clips").mkdir(parents=True, exist_ok=True)
    (d / "clips.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(out), "조각,", sum(len(c["say"]) - 9 for c in out), "글자")


def build(n):
    s, d = script(n), OUT / f"ep{n:02d}"
    m, src, tmp = ids(s), d / "clips", d / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    parts, t, lines, secs = [], 0.0, [], []

    def add(p):
        nonlocal t
        parts.append(p)
        t += dur(p)

    def silence(sec):
        p = tmp / f"s{len(parts):03d}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{sec}",
                        "-c:a", "pcm_s16le", str(p)], check=True)
        add(p)

    def sound(path, af):
        p = tmp / f"c{len(parts):03d}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-af", af, "-ar", str(SR), "-ac", "1",
                        "-c:a", "pcm_s16le", str(p)], check=True)
        add(p)

    # 앞뒤 무음을 자른 자리에서 소리가 갑자기 시작·끝나면 '딱' 잡음이 난다(2026-11-10 성범: wake up 앞 '삑').
    # 1화 이음새 162곳에 있었다. 앞 0.01초, 뒤 0.02초 페이드로 없앤다
    cut = ("silenceremove=start_periods=1:start_threshold=-45dB,afade=t=in:d=0.01,areverse,"
           "silenceremove=start_periods=1:start_threshold=-45dB,afade=t=in:d=0.02,areverse")
    # 시작음: 일레븐랩스 음악 MUSCInst-Cinematic_documentar (2026-11-10 성범 선택). 초급 시작음보다 약 3dB 작아서 덜 줄인다
    sound(RAW / "sfx-start-words.mp3", cut + ",volume=-6dB")
    silence(0.4)
    prev = None
    for key, who, text, ko, kind in steps(s):
        if prev and prev != key:
            silence(1.0)
            secs.append({"key": key, "title": {"words": "단어", "review": "복습", "outro": "끝인사"}[key], "start": round(t, 2)})
        elif not prev:
            secs.append({"key": key, "title": "도입", "start": round(t, 2)})
        elif kind == "word" or kind == "prompt" and lines[-1]["kind"] == "answer":
            if kind == "prompt":
                # 복습 문제 사이에는 말해보기처럼 짧은 클릭음을 넣는다.
                silence(0.4)
                sound(RAW / "sfx-next-soft.mp3", "atrim=0:1.0,afade=t=out:st=0.9:d=0.1,volume=-4dB")
                silence(0.3)
            else:
                silence(WORD_GAP)
        elif kind != "pause" and lines[-1]["kind"] != "pause":
            silence(GAP)
        if kind == "word":
            # 단어마다 시작에 클릭음 (2026-11-10 성범 선택: UIClick-soft,_appealing,_cli)
            sound(RAW / "sfx-word-click.mp3", cut + ",volume=-12dB")
            silence(0.3)
        prev = key
        if kind == "pause":
            a = t
            silence(PAUSE)
            lines.append({"section": key, "speaker": "나", "text": "직접 말해보세요", "meaning": None,
                          "kind": "pause", "start": round(a, 2), "end": round(t, 2)})
            continue
        a = t
        for k in range(REPEAT if kind == "repeat" else 1):
            if k:
                silence(REPEAT_GAP)
            cid = m[(who, text)]
            sound(src / f"{cid}.mp3", (f"atrim=start={SKIP[cid]},asetpts=PTS-STARTPTS," if cid in SKIP else "") + cut)
        lines.append({"section": key, "speaker": who, "text": text, "meaning": ko, "kind": "line" if kind == "repeat" else kind,  # word는 앱 가사에서 단어 묶음 사이를 띄우는 표시다
                      "start": round(a, 2), "end": round(t, 2)})
    silence(0.6)
    sound(RAW / "sfx-end.mp3", cut + ",volume=-9dB")

    listing = tmp / "list.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    mp3 = d / f"w1-{n:02d}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "1", "-c:a", "libmp3lame", "-b:a", "128k",
                    str(mp3)], check=True)
    webm = d / f"w1-{n:02d}.webm"  # 앱이 쓰는 소리. build_page.py가 app 폴더로 복사한다
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-ac", "1", "-c:a", "libopus", "-b:a", "24k", str(webm)], check=True)
    tl = {"title": s["title"], "duration": round(dur(webm), 2), "sections": secs, "lines": lines, "file": webm.name}
    (d / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    print(n, s["title"], f"{tl['duration']:.1f}초", len(lines), "줄")


if __name__ == "__main__":
    {"clips": clips, "build": build}[sys.argv[1]](int(sys.argv[2]))
