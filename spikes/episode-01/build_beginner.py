"""초급 대본의 음성을 묶고 조립한다. 시험판 코드다.

plan: 인물별 생성 문장을 audio/season/beginner-plan.json에 쓴다.
build N: cuts.json과 words.json의 cN-인물 음성으로 초급 N화를 조립한다.
"""
import json
import re
import sys
from pathlib import Path

from build_season import LINE_GAP, SEASON, SPEAK_PAUSE, SR, Builder, Source, run
from season_manifest import DEFAULT, VOICE, plain, rows, sections

STORY = Path(__file__).parent.parent.parent / "content" / "stories" / "course-beginner.md"


# 화면에는 왼쪽 글자를 그대로 보여 주고, 음성만 오른쪽처럼 읽는다.
SPOKEN = {
    "'저는 ~예요'와 '저는 ~가 아니에요'": "'저는 무엇무엇이에요'와 '저는 무엇무엇이 아니에요'",
    "look은 ~해 보인다는": "look은 무엇처럼 보인다는",
    "붙어서 ~도,": "붙어서 무엇무엇도,",
    "Let's는 ~하자,": "Let's는 이것 하자,",
    "'지금 ~하고 있어요'라는 뜻의 I'm ~ing을": "'지금 무엇을 하고 있어요'라는 뜻의, I'm 뒤에 ing을 붙이는 말을",
    "'~에서 왔어요'라는": "'어디에서 왔어요'라는",
    "'~을 잘해요'라는": "'무엇을 잘해요'라는",
    "'~을 좋아해요'와 '~을 안 좋아해요'": "'무엇을 좋아해요'와 '무엇을 안 좋아해요'",
    "'~이 있어요'와 '~이 없어요'": "'무엇이 있어요'와 '무엇이 없어요'",
    "'~을 원해요'와 '~하고 싶어요'": "'무엇을 원해요'와 '무엇을 하고 싶어요'",
}


def spoken(text):
    for shown, said in SPOKEN.items():
        text = text.replace(shown, said)
    return text


def shown(text):
    for screen, said in SPOKEN.items():
        text = text.replace(said, screen)
    return text


def clean(raw):
    return plain(raw.split(" || ")[0])


def blocks():
    text = STORY.read_text(encoding="utf-8")
    return {int(b.split("화")[0]): sections(b) for b in re.split(r"^## ", text, flags=re.M)[1:]}


def check_spoken(who, text):
    """음성이 기호 이름으로 읽을 글자가 남아 있으면 돈이 들기 전에 멈춘다. 화면 글자는 SPOKEN에서 읽는 말을 정한다."""
    bad = re.findall(r"[~/=+*#&%@_<>|]", text)
    if bad:
        sys.exit(f"소리로 읽으면 어색한 기호 {bad}: {who}: {text}")


def plan():
    out = {}
    for n, sec in blocks().items():
        files = {}
        for part in "ABCD":
            for who, raw in rows(sec[part]):
                raw = spoken(raw.split(" || ")[0])
                key = plain(raw)
                check_spoken(who, key)
                lines = files.setdefault(who, [])
                if who != "해설자" and any(l["key"] == key for l in lines):
                    continue
                lines.append({"key": key, "say": raw if raw.startswith("[") else f"{DEFAULT[who]} {raw}"})
        for who, lines in files.items():
            out[f"c{n}-{who}"] = {"voice": VOICE[who], "keys": [l["key"] for l in lines],
                                  "prompt": "\n[pause]\n".join(l["say"] for l in lines)}
    (SEASON / "beginner-plan.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, f in out.items():
        print(name, len(f["keys"]), len(f["prompt"]))


def build(n):
    cuts = json.loads((SEASON / "cuts.json").read_text(encoding="utf-8"))
    words = json.loads((SEASON / "words.json").read_text(encoding="utf-8"))
    src = {}
    for name, c in cuts.items():
        if name.startswith(f"c{n}-"):
            for row, w in zip(c, words[name]):
                row["words"] = w
            src[name.split("-", 1)[1]] = Source(name, c)
    sec = blocks()[n]

    def pick(who, key):
        # 고쳐서 다시 만든 줄은 '인물2' 파일에 있다. 있으면 그쪽을 먼저 쓴다.
        fixed = src.get(who + "2")
        key = spoken(key)
        s = fixed if fixed and key in fixed.clips else src[who]
        return s, s.clips[key]

    replay = [r.split(" || ") for _, r in rows(sec["E"])]
    b = Builder(f"b{n}")
    b.sfx("sfx-start.mp3")
    b.silence(0.3)

    b.section("intro", "도입")
    for who, raw in rows(sec["A"]):
        b.narrate("intro", *pick(who, plain(raw)))
    b.silence(0.7)

    def dialogue(section, ko):
        for i, (who, raw) in enumerate(rows(sec["B"])):
            if i:
                b.silence(LINE_GAP)
            key = plain(raw)
            b.line(section, who, *pick(who, key), key, ko[i][1] if ko else None)

    b.section("dialogue", "대화")
    dialogue("dialogue", None)
    b.silence(0.8)

    b.section("commentary", "해설")
    for i, (who, raw) in enumerate(rows(sec["C"])):
        if i:
            b.silence(LINE_GAP)
        key = plain(raw)
        if who == "해설자":
            b.narrate("commentary", *pick(who, key))
        else:
            b.line("commentary", who, *pick(who, key), key, None)
    b.silence(0.7)

    b.section("practice", "예문과 말해보기")
    pr = rows(sec["D"])
    for i in range(0, len(pr) - 1, 2):
        ko = plain(pr[i][1])
        b.narrate("practice", *pick("해설자", ko), kind="prompt")
        start = b.t
        b.silence(SPEAK_PAUSE)
        b.lines.append({"section": "practice", "speaker": "나", "text": "직접 말해보세요", "meaning": None,
                        "kind": "pause", "start": round(start, 2), "end": round(b.t, 2)})
        who, key = pr[i + 1][0], clean(pr[i + 1][1])
        b.line("practice", who, *pick(who, key), key, ko, kind="answer")
        b.silence(0.5)
    b.narrate("practice", *pick("해설자", plain(pr[-1][1])))
    b.silence(0.7)

    b.section("replay", "대화 다시 듣기")
    dialogue("replay", replay)
    b.silence(0.5)
    b.sfx("sfx-end.mp3")

    for line in b.lines:
        line["text"] = shown(line["text"])

    out = SEASON / f"b1-{n:02d}.mp3"
    listing = b.dir / "list.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in b.parts), encoding="utf-8")
    run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", str(SR), "-ac", "1", "-c:a", "libmp3lame", "-b:a", "128k", str(out))
    (SEASON / f"b1-{n:02d}.json").write_text(json.dumps(
        {"duration": round(b.t, 2), "sections": b.sections, "lines": b.lines}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(n, f"{b.t:.1f}초", len(b.lines), out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    if sys.argv[1] == "plan":
        plan()
    else:
        build(int(sys.argv[2]))
