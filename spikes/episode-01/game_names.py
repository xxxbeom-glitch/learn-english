"""빈칸 고르기에서 빈칸으로 내지 않을 고유명사 목록을 게임 자료에 넣는다 (2026-11-14 성범 "내이름이나 랩퍼이름이나 쿠팡이나
이런 특정 브랜드 명사가 아닌 어휘학습을 위한 단어라면 뭐든 좋아").

build_pwa.py가 부른다. app/game-data.js의 `window.GAME_NAMES = [...];` 줄을 새로 쓴다(없으면 끝에 붙인다).
data_pack.py가 이 줄을 게임 묶음의 names로 R2에 올리므로, 목록을 고치면 APK 없이 publish_data.py로 반영된다.

고르는 규칙: 게임 문장 가운데(문장 첫 단어가 아닌 자리)에서 대문자로 시작하는 말. I, I'm 같은 말은 뺀다.
KEEP은 대문자지만 어휘 공부가 되는 말이라 목록에서 뺀다(성범과 정함: 요일, 언어, Americano, Wi-Fi 등).
앱은 대소문자까지 같은 말만 고유명사로 본다(Olive Young의 Young은 빠지고, 다른 문장의 young은 빈칸이 될 수 있다).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
APP = HERE / "app"
LEAD = re.compile(r"^(?:whoa|wow|ha|haha|oh|ah|aw|aww|ooh|ugh|hmm|damn|uh|um)\b\S*\s+", re.I)
EDGE = re.compile(r"^[^\w']+|[^\w']+$")
KEEP = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December",
        "English", "Korean", "Americano", "Wi-Fi", "AC", "K-pop", "OK", "TV"}
STOP = {"The", "A", "An", "Of", "And"}  # 'The Weeknd'의 The 같은 말. 다른 문장 첫머리의 The까지 빠지지 않게 뺀다


def find(bank):
    names = set()
    for en, *_ in bank:
        words = LEAD.sub("", en).split()
        for k, w in enumerate(words):
            c = EDGE.sub("", w)
            if k and c[:1].isupper() and not re.match(r"^I('|$)", c) and not re.search(r"[.!?]$", words[k - 1]):
                names.add(c)
    return sorted(names - KEEP - STOP)


def apply():
    js_path = APP / "game-data.js"
    js = js_path.read_text(encoding="utf-8")
    bank = json.loads(re.search(r"^window\.GAME_BANK = (.*);$", js, re.M).group(1))
    names = find(bank)
    line = "window.GAME_NAMES = " + json.dumps(names, ensure_ascii=False, separators=(",", ":")) + ";"
    if re.search(r"^window\.GAME_NAMES = .*;$", js, re.M):
        js = re.sub(r"^window\.GAME_NAMES = .*;$", lambda _: line, js, flags=re.M)
    else:
        js = js.rstrip("\n") + "\n" + line + "\n"
    js_path.write_text(js, encoding="utf-8")
    print("빈칸에서 뺄 고유명사", len(names), "개")
    return names


if __name__ == "__main__":
    print(apply())
