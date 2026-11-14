"""게임 팁을 앱 자료에 넣는다 (2026-11-14 성범 "앱에 넣어줘").

팁 글의 원본은 content/game/tips-*.md의 표 한 줄 `| 번호 | 종류 | 영어 문장 | 팁 |`이다(성범이 검수하는 그 파일).
build_pwa.py가 부른다. app/game-data.js의 `window.GAME_TIPS = {...};` 줄을 새로 쓰고(없으면 끝에 붙인다),
게임 목록(GAME_BANK)에 없는 문장의 팁은 이름을 알려 준다(뜻 고치기 등으로 문장 글자가 바뀌면 팁이 떨어지므로).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
APP = HERE / "app"
SRC = HERE.parent.parent / "content" / "game"
ROW = re.compile(r"^\|\s*\d+\s*\|\s*[^|]+\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")


def read_tips():
    tips = {}
    for f in sorted(SRC.glob("tips-*.md")):
        for line in f.read_text(encoding="utf-8").splitlines():
            m = ROW.match(line)
            if m and m.group(1) not in ("문장",):
                tips[m.group(1)] = m.group(2)
    return tips


def apply():
    js_path = APP / "game-data.js"
    js = js_path.read_text(encoding="utf-8")
    bank = {r[0] for r in json.loads(re.search(r"^window\.GAME_BANK = (.*);$", js, re.M).group(1))}
    tips = read_tips()
    lost = [en for en in tips if en not in bank]
    if lost:
        print("게임 목록에 없는 문장의 팁(앱에 안 보여요):", lost)
    tips = {en: t for en, t in tips.items() if en in bank}
    line = "window.GAME_TIPS = " + json.dumps(tips, ensure_ascii=False, separators=(",", ":")) + ";"
    if re.search(r"^window\.GAME_TIPS = .*;$", js, re.M):
        js = re.sub(r"^window\.GAME_TIPS = .*;$", lambda _: line, js, flags=re.M)
    else:
        js = js.rstrip("\n") + "\n" + line + "\n"
    js_path.write_text(js, encoding="utf-8")
    print("게임 팁", len(tips), "개")
    return tips


if __name__ == "__main__":
    apply()
