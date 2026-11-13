"""R2에 올릴 내용 묶음을 만든다 (2026-11-13 성범 요청: 대본·시간표, 게임 문장, 커버를 R2에서 받아 쓴다).

build_pwa.py가 web/index.html을 만들면서 부르고, 결과를 data-pack/에 쓴다. publish_data.py가 그 폴더를 R2의 data/에 올린다.
  manifest.json            목록. 판 번호 v(올린 날짜와 시간, 예 202611131305)와 아래 파일들의 이름
  content-지문.json        { eps: 시간표, scripts: 대본, mb: 전체 소리 크기 }. 소리 주소는 R2 주소 + ?v=지문이라 소리와 시간표가 한 판으로 묶인다
  game-지문.json           { ver, audio, bank }. app/game-data.js와 같은 내용
  cover-이름-지문.webp     app/cover-*.webp
파일 이름에 내용 지문이 들어가서 이름이 같으면 내용도 같다. 앱은 목록의 이름이 달라진 파일만 받는다.
판 번호: 지난번에 올린 것(data-published.json)과 파일 이름이 모두 같으면 그 번호를 그대로 쓰고, 하나라도 다르면 지금 시각으로 새로 매긴다.
"""
import hashlib
import json
import re
import shutil
import time
from pathlib import Path

HERE = Path(__file__).parent
APP = HERE / "app"
PACK = HERE / "data-pack"
PUBLISHED = HERE / "data-published.json"
DATA_URL = "https://pub-54e325ce90af4f1bad3644fc22432096.r2.dev/data/"
FMT = 1  # 묶음 모양이 바뀌어 옛 앱이 읽지 못하게 되면 올린다(template.html 부팅 코드의 FMT와 같아야 한다)


def sig(b):
    return hashlib.sha1(b).hexdigest()[:8]


def pack(body, mb):
    """body: 소리 주소를 R2 주소로 바꾼 뒤의 화면 본문. mb: 전체 소리 크기(MB). 목록(dict)을 돌려주고 data-pack/을 새로 쓴다."""
    def line(name):
        m = re.search(rf"^const {name} = (.*);$", body, re.M)
        if not m:
            raise SystemExit(f"본문에서 {name} 줄을 못 찾았어요.")
        return m.group(1)

    scripts = json.loads(line("SCRIPTS"))
    ids = [f"{e['course']}|{e['n']}|{bool(e.get('alt'))}|{bool(e.get('draft'))}" for e in scripts]
    if len(set(ids)) != len(ids):
        raise SystemExit("과정과 화 번호가 같은 화가 있어요. 들은 기록의 이름표가 겹쳐요: " + str([i for i in ids if ids.count(i) > 1][:4]))
    content = ('{"eps":' + line("EPS") + ',"scripts":' + line("SCRIPTS") + ',"mb":' + str(mb) + "}").encode("utf-8")
    js = (APP / "game-data.js").read_text(encoding="utf-8")
    names = (("ver", "GAME_VER"), ("audio", "GAME_AUDIO"), ("bank", "GAME_BANK"))
    g = {k: json.loads(re.search(rf"^window\.{n} = (.*);$", js, re.M).group(1)) for k, n in names}
    game = json.dumps(g, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    mf = {"fmt": FMT, "v": 0, "content": f"content-{sig(content)}.json", "game": f"game-{sig(game)}.json", "covers": {}}
    files = {mf["content"]: content, mf["game"]: game}
    for f in sorted(APP.glob("cover-*.webp")):
        b = f.read_bytes()
        name = f"{f.stem}-{sig(b)}.webp"
        mf["covers"][f.stem[6:]] = name
        files[name] = b
    old = json.loads(PUBLISHED.read_text(encoding="utf-8")) if PUBLISHED.exists() else {}
    same = {k: v for k, v in old.items() if k != "v"} == {k: v for k, v in mf.items() if k != "v"}
    mf["v"] = old["v"] if same else int(time.strftime("%Y%m%d%H%M"))
    if PACK.exists():
        shutil.rmtree(PACK)
    PACK.mkdir()
    for name, b in files.items():
        (PACK / name).write_bytes(b)
    (PACK / "manifest.json").write_text(json.dumps(mf, ensure_ascii=False), encoding="utf-8")
    return mf
