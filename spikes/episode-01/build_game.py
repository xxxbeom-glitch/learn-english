"""문장 게임의 문제 목록과 문제 소리를 만든다 (2026-11-13, 게임 2단계).

이미 만든 화의 소리(app/*.webm)에서 줄 구간을 잘라 app/game/NNNN.webm으로 두고,
문제 목록을 app/game-data.js(window.GAME_BANK)로 쓴다. 새로 음성을 만들지 않으므로 비용은 0이다.
시간표와 대본은 app/episode-01.html의 EPS, SCRIPTS에서 읽는다(R2와 폰에 있는 소리와 같은 시간표).

범위: 초급·심화·고급의 예문과 말해보기 정답, 쉐도잉 일곱 앨범의 대화 줄. 팟캐스트는 시간이 어림인 곳이 있어 뺀다.
조건: 3~14단어, 영어 글자만, 같은 문장은 한 번만.
뜻: 쉐도잉과 말해보기 정답은 줄에 붙은 뜻, 예문은 바로 뒤 해설 줄(문장이 둘이면 두 줄)을 쓴다.

쓰기: python build_game.py          목록과 소리 모두
      python build_game.py --list   목록만(소리는 그대로)
"""
import hashlib
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

APP = Path(__file__).parent / "app"
AUDIO_BASE = "https://pub-54e325ce90af4f1bad3644fc22432096.r2.dev/audio/"  # build_pwa.py와 같은 통
OUT = APP / "game"
COURSES = {"초급", "심화", "고급"}
PODCASTS = {"더 리플레이", "매디의 서울 여행"}
HARD = {"현지인처럼 욕하기", "항의와 언쟁"}  # 이 앨범의 문장은 한 단계 올린다
NARR = "해설자"
# 대화 속에서만 맞는 뜻 고치기(2026-11-13 성범 지적: "Yeah, born and raised."의 뜻에 영어에 없는 '서울'이 있었다).
# 쉐도잉의 뜻은 앞뒤 대화에 맞춘 번역이라, 문장 하나만 떼어 내면 영어에 없는 말이 들어 있을 수 있다. 찾는 대로 game-ko-fix.json에 더한다(2026-11-13 전체 1,294문장을 한 번 검수해 48개를 고쳤다)
KO_FIX = json.loads((Path(__file__).parent / "game-ko-fix.json").read_text(encoding="utf-8"))  # { 영어 문장: 고친 뜻 }
# 원본 줄 맨 앞에 삑(660Hz 순음, 약 0.07초)이 붙어 있는 문장의 시작 초 고치기(2026-11-13 성범 지적: "What are you into these days?").
# 음성을 만들 때 생긴 잡음이 원본 화의 소리에도 들어 있다. 삑이 끝나는 지점부터 자른다. { 영어 문장: 새 시작 초(원본 화 기준) }
CUT_FIX = json.loads((Path(__file__).parent / "game-cut-fix.json").read_text(encoding="utf-8"))
PAD_IN, PAD_OUT = 0.05, 0.12  # 줄 앞뒤로 조금 더 담는다(옆 줄과의 빈 시간의 절반까지만)


def words(en):
    return [w for w in (re.sub(r"^[^\w']+|[^\w']+$", "", x) for x in en.split()) if w]


def main():
    html = (APP / "episode-01.html").read_text(encoding="utf-8")
    get = lambda n: json.loads(re.search(rf"^const {n} = (.*);$", html, re.M).group(1))
    eps, scripts = get("EPS"), get("SCRIPTS")
    seen, bank, skipped = set(), [], {"길이": 0, "글자": 0, "뜻 없음": 0, "중복": 0}
    for i, (t, e) in enumerate(zip(eps, scripts)):
        course = e["course"]
        if course in PODCASTS or e.get("alt"):
            continue
        ls = t["lines"]
        for k, l in enumerate(ls):
            sp, kind, sec = l.get("speaker"), l.get("kind"), l.get("section")
            if course in COURSES:
                if sp == NARR or not (sec == "examples" and kind == "line" or sec == "practice" and kind == "answer"):
                    continue
            elif not (sec == "talk" and kind == "line" and sp in ("Me", "Partner")):
                continue
            en = l["text"].strip()
            ko = KO_FIX.get(en) or l.get("meaning")
            if not ko and sec == "examples":
                # 예문 뒤 해설 줄이 뜻이다. 문장이 둘이면 뜻도 두 줄로 나뉘어 있다
                n = max(1, len(re.findall(r"[.?!]+(?:\s|$)", en)))
                nxt = [x["text"] for x in ls[k + 1:k + 1 + n] if x.get("speaker") == NARR]
                ko = " ".join(nxt) if len(nxt) == n else None
            w = words(en)
            key = " ".join(w).lower()
            if not 3 <= len(w) <= 14:
                skipped["길이"] += 1
            elif not re.fullmatch(r"[A-Za-z' ,.?!-]+", en):
                skipped["글자"] += 1
            elif not ko or re.search(r"[A-Za-z]{2,}", ko) and sec == "examples":
                skipped["뜻 없음"] += 1  # 뜻 자리에 영어가 섞인 해설 줄이 오면 뜻이 아니라 설명이다
            elif key in seen:
                skipped["중복"] += 1
            else:
                seen.add(key)
                prev_end = max([x["end"] for x in ls[:k] if x.get("end") is not None and x["end"] <= l["start"]] or [0])
                next_start = min([x["start"] for x in ls[k + 1:] if x.get("start") is not None and x["start"] >= l["end"]] or [t["duration"]])
                a = l["start"] - min(PAD_IN, (l["start"] - prev_end) / 2)
                b = l["end"] + min(PAD_OUT, (next_start - l["end"]) / 2)
                a = max(a, CUT_FIX.get(en, a))
                bank.append({"en": en, "ko": ko, "ep": i, "s": round(a, 2), "e": round(b, 2), "up": course in HARD, "file": t["file"], "course": course})
    for n, q in enumerate(bank):
        q["clip"] = f"game/{n + 1:04d}.webm"

    by = {}
    for q in bank:
        by[q["course"]] = by.get(q["course"], 0) + 1
    print(len(bank), "문장", by)
    print("뺀 것", skipped)

    if "--list" not in sys.argv:
        OUT.mkdir(exist_ok=True)
        for f in OUT.glob("*.webm"):
            f.unlink()

        def src(f):
            # 시간표는 R2에 올라간 소리(주소의 ?v=지문) 기준이다. 로컬 파일이 그 판과 다르면(다른 작업이 로컬에서 다시 자른 쉐도잉 등) R2 주소에서 바로 자른다(2026-11-13)
            p = APP / f.split("/")[-1].split("?")[0]
            v = f.split("?v=")[-1] if "?v=" in f else None
            if p.exists() and (not v or hashlib.sha1(p.read_bytes()).hexdigest()[:8] == v):
                return str(p)
            return f

        def cut(q):
            d = q["e"] - q["s"]
            fade = f"afade=t=in:d=0.02,afade=t=out:st={max(0, d - 0.04):.2f}:d=0.04"
            r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{q['s']:.2f}", "-t", f"{d:.2f}", "-i", src(q["file"]),
                                "-af", fade, "-ac", "1", "-c:a", "libopus", "-b:a", "32k", str(APP / q["clip"])], capture_output=True, text=True)
            return r.stderr.strip()

        with ThreadPoolExecutor(8) as ex:
            errs = [x for x in ex.map(cut, bank) if x]
        size = sum(f.stat().st_size for f in OUT.glob("*.webm"))
        print(len(list(OUT.glob("*.webm"))), "소리", size // 1024, "KB", "오류", len(errs), errs[:2])

    rows = [[q["en"], q["ko"], q["ep"], q["s"], q["e"], 1 if q["up"] else 0] for q in bank]
    js = "/* build_game.py가 만든다. 한 줄 = [영어, 뜻, 화 자리 번호, 시작 초, 끝 초, 한 단계 올림]. 소리는 game/NNNN.webm(줄 순서대로) */\n"
    data = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    # 소리는 R2의 audio/game/에서 받는다(upload_game_r2.py로 올림). 문장이나 자른 구간이 바뀌면 GAME_VER이 바뀌어 폰이 새로 받는다(뜻만 고치면 그대로)
    js += f'window.GAME_AUDIO = "{AUDIO_BASE}game/";\nwindow.GAME_VER = "{hashlib.sha1(json.dumps([[q["en"], q["ep"], q["s"], q["e"]] for q in bank]).encode()).hexdigest()[:8]}";\n'
    js += "window.GAME_BANK = " + data + ";\n"
    (APP / "game-data.js").write_text(js, encoding="utf-8")
    print("app/game-data.js", len(js.encode("utf-8")) // 1024, "KB")


if __name__ == "__main__":
    main()
