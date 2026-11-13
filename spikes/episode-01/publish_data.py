"""내용 묶음(data-pack/)을 Cloudflare R2(side-a-audio 통)의 data/에 올린다 (2026-11-13 성범 요청).

python build_pwa.py      먼저 묶음을 만든다(data_pack.py)
python publish_data.py   바뀐 파일만 올리고, 목록(manifest.json)을 맨 마지막에 올린다

목록을 마지막에 올려서, 앱이 새 목록을 본 때에는 내용 파일이 이미 다 올라가 있다.
소리가 바뀌었으면 upload_r2.py(화의 소리)와 upload_game_r2.py(게임 소리)를 먼저 돌린다. 그래야 새 시간표와 새 소리가 같은 판으로 묶인다.
올린 뒤에는 폰에서 앱을 다시 켜면 설치 없이 반영된다. 환경 변수 SIDEA_WRANGLER에 wrangler.js 경로를 주면 빨리 올라간다(upload_game_r2.py와 같다).
"""
import json
import os
import subprocess
import sys

from data_pack import PACK, PUBLISHED
from upload_r2 import ACCOUNT, BUCKET

_W = os.environ.get("SIDEA_WRANGLER")
WRANGLER = ["node", _W] if _W else ["npx", "-y", "wrangler@latest"]
SHELL = not _W and sys.platform == "win32"
TYPES = {".json": "application/json", ".webp": "image/webp"}


def put(f, cache):
    r = subprocess.run([*WRANGLER, "r2", "object", "put", f"{BUCKET}/data/{f.name}", "--file", str(f), "--remote",
                        "--content-type", TYPES[f.suffix], "--cache-control", cache],
                       env=os.environ | {"CLOUDFLARE_ACCOUNT_ID": ACCOUNT}, capture_output=True, text=True, encoding="utf-8", shell=SHELL)
    if r.returncode:
        sys.exit(f"실패: {f.name} {(r.stderr or r.stdout)[-500:]}")


def main():
    mf = json.loads((PACK / "manifest.json").read_text(encoding="utf-8"))
    old = json.loads(PUBLISHED.read_text(encoding="utf-8")) if PUBLISHED.exists() else {}
    if old == mf:
        print("바뀐 것이 없어요. 판", mf["v"])
        return
    had = {old.get("content"), old.get("game"), old.get("albums"), *old.get("covers", {}).values()}
    todo = [f for f in [mf["content"], mf["game"], mf["albums"], *mf["covers"].values()] if f not in had]
    for k, name in enumerate(todo, 1):
        put(PACK / name, "public, max-age=31536000, immutable")  # 이름에 지문이 있어 내용이 바뀌지 않는다
        print(f"{k}/{len(todo)} {name}", flush=True)
    put(PACK / "manifest.json", "no-store")
    PUBLISHED.write_text(json.dumps(mf, ensure_ascii=False, indent=1), encoding="utf-8")
    print("올렸어요. 판", mf["v"])


if __name__ == "__main__":
    main()
