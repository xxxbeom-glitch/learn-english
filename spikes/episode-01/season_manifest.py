"""시즌 1 Part 1 대본을 인물별 생성 묶음으로 나눈다. 시험판 코드다.

화마다 인물별로 대사를 한 번씩만 모은다. 같은 문장은 한 번만 만들고 재사용한다.
결과는 audio/season/manifest.json에 쓴다.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
STORY = HERE.parent.parent / "content" / "stories" / "season-1-part-1.md"
OUT = HERE / "audio" / "season" / "manifest.json"
TAG = re.compile(r"\[[^\]]*\]\s*")
# 태그는 다음 태그까지 이어지므로, 태그 없는 줄에는 인물의 기본 말투를 붙인다.
DEFAULT = {"해설자": "[casual]", "성범": "[calm]", "Harry": "[casual]", "Olivia": "[calm]", "지수": "[casual]",
           "Jay": "[casual]", "Officer": "[neutral]", "Clerk": "[casual]", "Staff": "[friendly]", "Server": "[upbeat]"}
VOICE = {
    "해설자": "aiUUgjHa4mpHf6UenZuf", "성범": "7EzWGsX10sAS4c9m9cPf", "Harry": "bIHbv24MWmeRgasZH58o",
    "Olivia": "vppqTjjplEh4CplGZuN2", "지수": "vhhJX7dyal9WlYW2UAsj",
    "Jay": "OYTbf65OHHFELVut7v2H", "Officer": "cjVigY5qzO86Huf0OWal", "Clerk": "ZoiZ8fuDWInAcwPXaVeq",
    "Staff": "ZIlrSGI4jZqobxRKprJz", "Server": "Bwff1jnzl1s94AEcntUq",
}


def plain(text):
    return re.sub(r"\s+", " ", TAG.sub("", text)).strip()


def rows(block):
    return [l.split(": ", 1) for l in block.split("\n") if ": " in l and not l.startswith(("(", "첫 대화"))]


def sections(body):
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"### ([A-E])\. [^\n]*\n(.*?)(?=\n### |\Z)", body, re.S)}


def main():
    text = STORY.read_text(encoding="utf-8")
    eps = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        n = int(block.split("화")[0])
        sec = sections(block)
        files = {}

        def add(who, raw):
            key = plain(raw)
            lines = files.setdefault(who, [])
            if who != "해설자" and any(l["key"] == key for l in lines):
                return
            tagged = raw if raw.startswith("[") else f"{DEFAULT[who]} {raw}"
            lines.append({"key": key, "say": tagged})

        for part in ("A", "B", "C"):
            for who, raw in rows(sec[part]):
                add(who, raw)
        eps.append({"n": n, "files": [
            {"who": who, "voice": VOICE[who], "lines": lines,
             "prompt": "\n[pause]\n".join(l["say"] for l in lines)}
            for who, lines in files.items()]})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(eps, ensure_ascii=False, indent=1), encoding="utf-8")
    for e in eps:
        for f in e["files"]:
            print(e["n"], f["who"], len(f["lines"]), len(f["prompt"]))
    print(sum(len(f["prompt"]) for e in eps for f in e["files"]))


if __name__ == "__main__":
    main()
