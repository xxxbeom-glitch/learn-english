"""template.html의 화면 코드만 바꿔 app/episode-01.html을 다시 만든다. 대본·시간표·커버 데이터는 지금 있는 episode-01.html에서 그대로 가져온다.
앨범 목록은 albums.json에서 읽어 넣는다(2026-11-13).

build_page.py를 돌리면 자른 쉐도잉 시간표가 들어가 R2에 올라가 있는 옛 소리와 어긋난다(2026-11-12).
그래서 폰에 넣을 때는 build_page.py 대신 이것을 돌리고, 이어서 build_pwa.py를 돌린다.
"""
import re
from pathlib import Path

from data_pack import albums_line

APP = Path(__file__).parent / "app"


def main():
    old = (APP / "episode-01.html").read_text(encoding="utf-8")
    t = (APP / "template.html").read_text(encoding="utf-8")

    def line(name):
        m = re.search(rf"^const {name} = (.*);$", old, re.M)
        if not m:
            raise SystemExit(f"episode-01.html에서 {name} 줄을 못 찾았어요.")
        return m.group(1)

    p = re.search(r"const P = (\d+),", old)
    if not p:
        raise SystemExit("episode-01.html에서 POD_AT 값을 못 찾았어요.")
    out = t
    for key, val in [("__TIMELINE__", line("EPS")), ("__SCRIPTS__", line("SCRIPTS")), ("__COVERS__", line("COVERS")), ("__POD_AT__", p.group(1)), ("__ALBUMS__", albums_line())]:
        if out.count(key) != 1:
            raise SystemExit(f"template.html에 {key} 자리가 하나가 아니에요.")
        out = out.replace(key, val)
    (APP / "episode-01.html").write_text(out, encoding="utf-8")
    print("app/episode-01.html", len(out) // 1024, "KB")


if __name__ == "__main__":
    main()
