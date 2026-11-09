"""앱 페이지 조립 스크립트. 시간표와 시즌 대본을 템플릿에 넣는다. 버리는 코드다."""
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
STORY = HERE.parent.parent / "content" / "stories" / "season-1-part-1.md"
STORY_KO = HERE.parent.parent / "content" / "stories" / "season-1-part-1-ko.md"
BEGINNER = HERE.parent.parent / "content" / "stories" / "course-beginner.md"
DRAFT = HERE.parent.parent / "content" / "stories" / "beginner-08-16-ko-draft.md"
WHO = {"Harry": "해리", "Olivia": "올리비아", "지수": "지수", "성범": "성범", "해설자": "해설자",
       "Jay": "제이", "Officer": "심사관", "Clerk": "점원", "Staff": "직원", "Server": "종업원",
       "남1": "남1", "남2": "남2", "여1": "여1", "여2": "여2"}
SECTIONS = {"A. 대화": "대화", "B. 해설": "해설", "C. 말해보기": "말해보기", "D. 대화 다시 듣기": "대화 다시 듣기",
            "A. 도입": "도입", "B. 대화": "대화", "C. 해설": "해설", "D. 예문과 말해보기": "예문과 말해보기", "E. 대화 다시 듣기": "대화 다시 듣기",
            "도입": "도입", "예문": "예문", "정리": "정리", "말해보기": "말해보기"}
# 2026-11-09 초급 새 짜임(도입, 예문, 정리, 말해보기). 음성을 만들기 전이라 글 길이로 시간을 어림잡고, 소리 없는 파일을 붙인다.
TEXT_KEYS = {"도입": "intro", "예문": "examples", "정리": "wrap", "말해보기": "practice"}


def say_time(who, text):
    """음성이 없을 때 쓰는 어림 시간(초). 한국어 해설은 글자 수, 영어는 단어 수로 잡는다."""
    if who == "해설자":
        return max(1.0, len(text) * 0.16)
    return 0.6 + len(text.split()) * 0.32


def text_timeline(e):
    """대본만 있는 화의 시간표. 해설은 문장마다 한 줄로 나눈다."""
    t, lines, secs = 1.0, [], []
    for s in e["sections"]:
        key = TEXT_KEYS[s["title"]]
        if secs:
            t += 0.6
        secs.append({"key": key, "title": s["title"], "start": round(t, 2)})
        src = s["lines"]
        for k, l in enumerate(src):
            if l.get("pause"):
                lines.append({"section": key, "speaker": "나", "text": "직접 말해보세요", "meaning": None,
                              "kind": "pause", "start": round(t, 2), "end": round(t + 3, 2)})
                t += 3
                continue
            prompt = key == "practice" and k + 1 < len(src) and src[k + 1].get("pause")
            answer = key == "practice" and k > 0 and src[k - 1].get("pause")
            parts = [l["text"]] if l["who"] != "해설자" or prompt else re.split(r"(?<=[.?!])\s+", l["text"])
            for p in parts:
                d = say_time(l["who"], p)
                lines.append({"section": key, "speaker": l["who"], "text": p,
                              "meaning": l["ko"] if answer else None,
                              "kind": "prompt" if prompt else "answer" if answer else "line",
                              "start": round(t, 2), "end": round(t + d, 2)})
                t += d + 0.35
    dur = round(t + 0.7, 1)
    name = f"b1-{e['n']:02d}-text.webm"
    out = HERE / "app" / name
    stamp = out.with_suffix(".len")
    if not out.exists() or not stamp.exists() or stamp.read_text() != str(dur):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono",
                        "-t", str(dur), "-c:a", "libopus", "-b:a", "6k", str(out)], check=True)
        stamp.write_text(str(dur))
    return {"duration": dur, "sections": secs, "lines": lines, "file": name}


def parse(text):
    eps = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head, *rest = block.split("\n")
        n, title = re.match(r"(\d+)화\. (.+)", head).groups()
        ep = {"n": int(n), "title": title, "keys": [], "again": [], "sections": [], "notes": []}
        sec, in_notes = None, False
        for raw in rest:
            line = raw.strip()
            if line.startswith("### "):
                in_notes = line[4:] == "E. 화면 해설"
                sec = None if in_notes else {"title": SECTIONS[line[4:]], "lines": []}
                if sec:
                    ep["sections"].append(sec)
            elif in_notes and raw.startswith("  - "):
                tag, body = line[2:].split(":", 1)
                en, ko = [x.strip() for x in body.split("||", 1)]
                ep["notes"][-1]["more"].append([tag, en, ko])
            elif in_notes and line.startswith("- "):
                en, ko, body = [x.strip() for x in line[2:].split("||")]
                ep["notes"].append({"en": en, "ko": ko, "body": body, "more": []})
            elif line.startswith("- 인물: "):
                ep["cast"] = [x.strip() for x in line[6:].split(",") if x.strip() != "성범"]
            elif line.startswith("- Key Points: "):
                ep["keys"] = re.findall(r"`([^`]+)`", line)
            elif line.startswith("- 다시 쓰는 문장: "):
                first = int(re.search(r"\((\d+)화\)", line).group(1))
                ep["again"] += [{"en": en, "ep": first} for en in re.findall(r"`([^`]+)`", line)]
            elif line == "(멈춤 3초)":
                sec["lines"].append({"pause": True})
            elif sec is not None and ": " in line and line.split(": ", 1)[0] in WHO:
                who, say = line.split(": ", 1)
                say = re.sub(r"\[[^\]]*\]\s*", "", say).strip()
                say, _, ko = say.partition(" || ")
                sec["lines"].append({"who": WHO[who], "text": say, "ko": ko or None})
        eps.append(ep)
    return eps


def parse_ko(text):
    out = {}
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head, *rest = block.split("\n")
        n, title = re.match(r"(\d+)화\. (.+)", head).groups()
        out[int(n)] = {"title": title, "lines": [dict(zip(("who", "text"), l.split(": ", 1))) for l in rest if ": " in l]}
    return out


def parse_draft(text):
    """대화 초안: '## 8화. 패턴' 아래 '- 인물: 영어 || 한국어'."""
    out = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head, *rest = block.split("\n")
        n, title = re.match(r"(\d+)화\. (.+)", head).groups()
        title = re.sub(r"\s*\(.*\)$", "", title).strip()
        lines = []
        for raw in rest:
            m = re.match(r"- (\S+): (.+)", raw.strip())
            if m:
                en, _, ko = m.group(2).partition(" || ")
                lines.append({"who": m.group(1), "text": en.strip(), "ko": ko.strip() or None})
        out.append((int(n), title, lines))
    return out


def main():
    t = (HERE / "app" / "template.html").read_text(encoding="utf-8")
    eps, tl = [], []
    # 앱에는 새 과정의 화만 넣는다. 시간표와 대본의 순서를 같게 둔다.
    # 2026-11-09 초급을 새 짜임으로 다시 썼다. 옛 음성(b1-NN.webm)은 새 대본과 맞지 않아 쓰지 않고,
    # 음성을 만들 때까지 글 길이로 어림한 시간표와 소리 없는 파일로 대본을 보여 준다.
    # 화 수(25)와 순서는 그대로라 폰에 저장된 들은 기록의 자리 번호는 밀리지 않는다.
    for e in parse(BEGINNER.read_text(encoding="utf-8")):
        e["kolines"] = []
        e["course"] = "초급"
        e["text"] = True
        eps.append(e)
        tl.append(text_timeline(e))
    # 팟캐스트 앨범(build_podcast.py가 만든 시간표). 시간표와 대본은 같은 자리에 있어야 하므로,
    # 음성 있는 화 바로 뒤, 음성 없는 화 앞에 끼운다. 앨범 이름(course)은 템플릿의 PODCASTS와 같아야 한다.
    # 주의: 초급 화의 음성이 새로 생기면 팟캐스트 트랙의 자리 번호가 밀려, 폰에 저장된 들은 기록이 어긋날 수 있다.
    pods_e, pods_t = [], []
    # 앨범 번호(r1, r2 ...)마다 이름과 출연자. 새 앨범은 기존 앨범 뒤에 붙어서 앞 트랙의 자리 번호를 밀지 않는다.
    albums = {"r1": ("드레이크 vs 켄드릭", ["마이크", "데이나"]), "r2": ("영떡과 YSL 재판", ["마이크", "타샤"])}
    for src in sorted((HERE / "audio" / "podcast").glob("r*-*.json")):
        p = json.loads(src.read_text(encoding="utf-8"))
        al, n = src.stem.split("-")
        course, cast = albums[al]
        pods_e.append({"n": int(n), "title": p["title"], "keys": [], "again": [], "notes": [], "sections": [],
                       "kolines": [], "cast": cast, "course": course})
        pods_t.append({k: v for k, v in p.items() if k != "title"} | {"file": f"{src.stem}.webm"})
    k = len(tl)
    eps[k:k] = pods_e
    tl += pods_t
    # 해설을 쓰기 전의 화는 대화만 대본에 넣는다.
    have = {e["n"] for e in eps if e["course"] == "초급"}
    for n, title, lines in parse_draft(DRAFT.read_text(encoding="utf-8")) if DRAFT.exists() else []:
        if n not in have:
            eps.append({"n": n, "title": title, "keys": [], "again": [], "notes": [],
                        "sections": [{"title": "대화", "lines": lines}],
                        "kolines": [{"who": l["who"], "text": l["ko"]} for l in lines],
                        "course": "초급", "draft": True})
    # 화면 글자에서는 한국인 이름을 한글로 통일한다. 음성은 대본 원문(Seongbeom)으로 만들었으므로 원문은 그대로 둔다.
    # (2026-11-08 성범 지적: 어떤 줄은 성범, 어떤 줄은 Seongbeom)
    def shown(x):
        return json.dumps(x, ensure_ascii=False).replace("Seongbeom", "성범")
    out = t.replace("__TIMELINE__", shown(tl)).replace("__SCRIPTS__", shown(eps))
    (HERE / "app" / "episode-01.html").write_text(out, encoding="utf-8")
    print(len(eps), [sum(len(s["lines"]) for s in e["sections"]) for e in eps])


if __name__ == "__main__":
    main()
