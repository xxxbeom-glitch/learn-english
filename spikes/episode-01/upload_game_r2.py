"""문장 게임의 문제 소리(app/game/*.webm)를 Cloudflare R2(side-a-audio 통)의 audio/game/에 올린다.

python upload_game_r2.py

build_game.py로 소리를 자른 뒤 실행한다. 이미 같은 내용으로 올린 파일(r2-uploaded-game.json의 내용 지문이 같은 것)은 건너뛴다.
파일이 1,300개쯤이라 여덟 개씩 동시에 올린다. 통과 계정은 upload_r2.py와 같다. 2026-11-13 성범 요청으로 앱 안에 넣던 것을 R2로 옮겼다.
"""
import hashlib
import json
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from upload_r2 import ACCOUNT, BUCKET

HERE = Path(__file__).parent
GAME = HERE / "app" / "game"
DONE = HERE / "r2-uploaded-game.json"
LOCK = threading.Lock()
# npx는 부를 때마다 느리다. 환경 변수 SIDEA_WRANGLER에 설치해 둔 wrangler.js 경로를 주면 node로 바로 불러 훨씬 빠르다
_W = os.environ.get("SIDEA_WRANGLER")
WRANGLER = ["node", _W] if _W else ["npx", "-y", "wrangler@latest"]
SHELL = not _W and sys.platform == "win32"
WORKERS = 16 if _W else 8


def main():
    files = sorted(GAME.glob("*.webm"))
    done = json.loads(DONE.read_text(encoding="utf-8")) if DONE.exists() else {}
    sig = {f.name: hashlib.sha1(f.read_bytes()).hexdigest()[:8] for f in files}
    todo = [f for f in files if done.get(f.name) != sig[f.name]]
    if len(sys.argv) > 1:
        todo = todo[:int(sys.argv[1])]
    print(f"{len(files)}개 중 {len(todo)}개를 올린다", flush=True)
    env = os.environ | {"CLOUDFLARE_ACCOUNT_ID": ACCOUNT}
    fails = []

    def put(f):
        for _ in range(3):
            r = subprocess.run([*WRANGLER, "r2", "object", "put", f"{BUCKET}/audio/game/{f.name}", "--file", str(f),
                                "--remote", "--content-type", "audio/webm", "--cache-control", "public, max-age=86400"],
                               env=env, capture_output=True, text=True, encoding="utf-8", shell=SHELL)
            if not r.returncode:
                with LOCK:
                    done[f.name] = sig[f.name]
                    if len(done) % 25 == 0:
                        DONE.write_text(json.dumps(done, indent=1, sort_keys=True), encoding="utf-8")
                        print(len(done), "/", len(files), flush=True)
                return
        fails.append((f.name, (r.stderr or r.stdout)[-300:]))

    with ThreadPoolExecutor(WORKERS) as ex:
        list(ex.map(put, todo))
    DONE.write_text(json.dumps(done, indent=1, sort_keys=True), encoding="utf-8")
    print("끝. 올린 것", len(done), "실패", len(fails), fails[:2])


if __name__ == "__main__":
    main()
