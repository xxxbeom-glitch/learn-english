"""초급 새 짜임(2026-11-09) 음성. 시험판 코드다.

clips N: 화 N에서 만들 음성 조각 목록을 audio/beginner2/epNN/clips.json에 쓴다.
          같은 목소리의 같은 영어 문장은 한 번만 만든다. 해설자는 대본 한 줄이 한 조각이다.
build N:  조각 MP3(audio/beginner2/epNN/clips/<id>.mp3)를 이어 붙여
          app/b1-NN-v2.webm과 시간표(audio/beginner2/epNN/timeline.json)를 만든다.
          조각 길이를 재서 시간을 잡으므로 받아쓰기(단어 시간)는 쓰지 않는다.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from build_page import BEGINNER, TEXT_KEYS, parse

HERE = Path(__file__).parent
OUT = HERE / "audio" / "beginner2"
SOUNDS = OUT  # 조각은 audio/beginner2/epNN/clips/에 둔다 (2026-11-09 성범: learn-english 폴더에 저장)
RAW = HERE / "audio" / "raw"
APP = HERE / "app"
SR = 44100

# 남1 Jack John(옛 성범), 여1 Hope(옛 제이), 남2 Will(옛 해리), 여2 Clara(옛 가게 직원). (작성자 판단)
VOICE = {"해설자": "aiUUgjHa4mpHf6UenZuf", "남1": "7EzWGsX10sAS4c9m9cPf", "여1": "OYTbf65OHHFELVut7v2H",
         "남2": "bIHbv24MWmeRgasZH58o", "여2": "ZIlrSGI4jZqobxRKprJz"}
DEFAULT = {"해설자": "[casual]", "남1": "[casual]", "여1": "[casual]", "남2": "[casual]", "여2": "[casual]"}
# 문장마다 말투를 바꿀 때만 적는다.
TAG = {"I'm so excited!": "[excited]", "I'm so sore.": "[tired]", "I'm broke.": "[sighs]", "I'm tired.": "[tired]",
       "I'm late.": "[worried]", "Sorry, I'm late.": "[worried]","I'm not ready.": "[nervous]"}
SAY = {"R&B": "R and B"}
GAP, AFTER_PAIR, SECTION_GAP, PAUSE = 0.4, 0.8, 1.0, 3.0


def episode(n):
    return next(e for e in parse(BEGINNER.read_text(encoding="utf-8")) if e["n"] == n)


def items(e):
    """대본 순서대로 (구간, 줄, 조각 id, 종류)를 낸다."""
    ids = {}
    for s in e["sections"]:
        key = TEXT_KEYS[s["title"]]
        src = s["lines"]
        for k, l in enumerate(src):
            if l.get("pause"):
                yield key, l, None, "pause"
                continue
            prompt = key == "practice" and k + 1 < len(src) and src[k + 1].get("pause")
            answer = key == "practice" and k > 0 and src[k - 1].get("pause")
            if l["who"] == "해설자":
                cid = f"n{len([i for i in ids if i.startswith('n')]) + 1:02d}"
                ids[cid] = l
            else:
                same = next((i for i, x in ids.items() if x["who"] == l["who"] and x["text"] == l["text"]), None)
                cid = same or f"e{len([i for i in ids if i.startswith('e')]) + 1:02d}"
                ids[cid] = l
            yield key, l, cid, "prompt" if prompt else "answer" if answer else "line"


def clips(n):
    e, seen, out = episode(n), set(), []
    for _, l, cid, _ in items(e):
        if cid and cid not in seen:
            seen.add(cid)
            say = l["text"]
            for shown, spoken in SAY.items():  # 화면 글자는 그대로 두고 읽는 말만 바꾼다.
                say = say.replace(shown, spoken)
            bad = re.findall(r"[~/=+*#&%@_<>|]", say)
            if bad:
                sys.exit(f"소리로 읽으면 어색한 기호 {bad}: {l['text']}")
            out.append({"id": cid, "who": l["who"], "voice": VOICE[l["who"]],
                        "say": f"{TAG.get(l['text'], DEFAULT[l['who']])} {say}"})
    d = OUT / f"ep{n:02d}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "clips.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(out), "조각,", sum(len(c["say"]) for c in out), "글자")


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                check=True, capture_output=True, text=True).stdout)


# 비교용 판: 영어 조각만 다른 엔진으로 바꾼다. 한국어 해설 조각은 원래 것을 그대로 쓴다. (2026-11-09 성범 요청)
# 판 이름: (조각 폴더, 바꿀 조각 id 머리글자). g는 영어만, gk는 한국어 해설까지 구글 Gemini 3.8 Flash TTS.
GOOGLE = HERE / "audio" / "google-test" / "gemini-3.8-flash-tts-v2"
VARIANTS = {"g": (GOOGLE, ("e",)), "gk": (GOOGLE, ("e", "n"))}


def build(n, var=""):
    e = episode(n)
    d = OUT / f"ep{n:02d}{var}"
    src, tmp = SOUNDS / f"ep{n:02d}" / "clips", d / "tmp"
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

    def sound(path, extra="", trim=True):
        p = tmp / f"c{len(parts):03d}.wav"
        # 앞뒤 침묵을 다듬어 조각 사이 간격을 일정하게 한다.
        cut = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-af", (cut + extra) if trim else (extra or "anull"), "-ar", str(SR), "-ac", "1",
                        "-c:a", "pcm_s16le", str(p)], check=True)
        add(p)

    sound(RAW / "sfx-start.mp3", ",volume=-9dB")
    silence(0.4)
    prev = None
    for key, l, cid, kind in items(e):
        if prev and prev != key:
            silence(SECTION_GAP)
        if not prev or prev != key:
            title = next(k for k, v in TEXT_KEYS.items() if v == key)
            secs.append({"key": key, "title": title, "start": round(t, 2)})
        elif kind != "pause" and lines and lines[-1]["kind"] != "pause":
            # 예문(영어+해설)과 말해보기(한국어+멈춤+영어)는 한 쌍이다. 쌍 사이는 조금 더 띄운다.
            if kind == "prompt" and lines[-1]["kind"] == "answer":
                # 말해보기 문제 사이에 짧은 "띵"을 넣어 다음 문제로 넘어감을 알린다. (2026-11-09 성범 요청)
                # 소리: 일레븐랩스 효과음 라이브러리 클릭 카테고리 "Create a very soft U..." (성범 선택).
                # 파일은 2초인데 소리는 앞 1초뿐이라 1초에서 자르고, 목소리보다 튀지 않게 4dB 줄인다.
                silence(0.4)
                sound(RAW / "sfx-next-soft.mp3", "atrim=0:1.0,afade=t=out:st=0.9:d=0.1,volume=-4dB", trim=False)
                silence(0.3)
            else:
                silence(AFTER_PAIR if (key == "examples" and l["who"] != "해설자") or kind == "prompt" else GAP)
        prev = key
        if kind == "pause":
            a = t
            silence(PAUSE)
            lines.append({"section": key, "speaker": "나", "text": "직접 말해보세요", "meaning": None,
                          "kind": "pause", "start": round(a, 2), "end": round(t, 2)})
            continue
        a = t
        sound((VARIANTS[var][0] if var and cid.startswith(VARIANTS[var][1]) else src) / f"{cid}.mp3")
        b = t
        if l["who"] == "해설자" and kind != "prompt":
            # 해설 한 줄을 문장으로 나누고, 글자 수에 비례해 시간을 나눈다.
            sents = re.split(r"(?<=[.?!])\s+", l["text"])
            total = sum(len(s) for s in sents)
            x = a
            for i, s in enumerate(sents):
                y = b if i == len(sents) - 1 else x + (b - a) * len(s) / total
                lines.append({"section": key, "speaker": "해설자", "text": s, "meaning": None, "kind": "line",
                              "start": round(x, 2), "end": round(y, 2)})
                x = y
        else:
            lines.append({"section": key, "speaker": l["who"], "text": l["text"],
                          "meaning": l["ko"] if kind == "answer" else None, "kind": kind,
                          "start": round(a, 2), "end": round(b, 2)})
    silence(0.6)
    sound(RAW / "sfx-end.mp3", ",volume=-9dB")

    listing = tmp / "list.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    mp3 = d / f"b1-{n:02d}-v2{var}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "1", "-c:a", "libmp3lame", "-b:a", "128k",
                    str(mp3)], check=True)
    name = f"b1-{n:02d}-v2{var}.webm"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-ac", "1", "-c:a", "libopus", "-b:a", "24k",
                    str(APP / name)], check=True)
    tl = {"duration": round(dur(APP / name), 2), "sections": secs, "lines": lines, "file": name}
    (d / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    print(n, f"{tl['duration']:.1f}초", len(lines), "줄")


def timeline(n, var=""):
    """만들어 둔 음성 시간표가 있으면 돌려준다."""
    p = OUT / f"ep{n:02d}{var}" / "timeline.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() and (APP / f"b1-{n:02d}-v2{var}.webm").exists() else None


if __name__ == "__main__":
    {"clips": clips, "build": build}[sys.argv[1]](int(sys.argv[2]), *sys.argv[3:])
