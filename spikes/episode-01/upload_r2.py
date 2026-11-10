"""앱이 쓰는 소리 파일을 Cloudflare R2(side-a-audio 통)에 올린다.

python upload_r2.py

build_page.py로 app/episode-01.html을 만든 뒤 실행한다. 화면이 실제로 쓰는 app/*.webm만 올리고,
이미 같은 내용으로 올린 파일(r2-uploaded.json에 내용 지문이 같은 것)은 건너뛴다.
통 주소는 build_pwa.py의 AUDIO_BASE와 같다. 2026-11-10 성범 요청으로 앱 안에 넣던 소리를 R2로 옮겼다.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
APP = HERE / "app"
DONE = HERE / "r2-uploaded.json"
BUCKET = "side-a-audio"
ACCOUNT = "4dca8890d93f9b7b8aeb2d04125427ff"  # Psblove88 계정. wrangler 로그인에 계정이 둘이라 꼭 붙인다


def main():
    body = (APP / "episode-01.html").read_text(encoding="utf-8")
    files = [f for f in sorted(APP.glob("*.webm")) if f'"{f.name}"' in body]
    done = json.loads(DONE.read_text(encoding="utf-8")) if DONE.exists() else {}
    env = os.environ | {"CLOUDFLARE_ACCOUNT_ID": ACCOUNT}
    todo = [f for f in files if done.get(f.name) != hashlib.sha1(f.read_bytes()).hexdigest()[:8]]
    print(f"{len(files)}개 중 {len(todo)}개를 올린다")
    for k, f in enumerate(todo, 1):
        h = hashlib.sha1(f.read_bytes()).hexdigest()[:8]
        r = subprocess.run(["npx", "-y", "wrangler@latest", "r2", "object", "put", f"{BUCKET}/audio/{f.name}", "--file", str(f),
                            "--remote", "--content-type", "audio/webm", "--cache-control", "public, max-age=86400"],
                           env=env, capture_output=True, text=True, encoding="utf-8", shell=sys.platform == "win32")
        if r.returncode:
            print("실패:", f.name, r.stderr[-500:]); sys.exit(1)
        done[f.name] = h
        DONE.write_text(json.dumps(done, indent=1, sort_keys=True), encoding="utf-8")
        print(f"{k}/{len(todo)} {f.name}")


if __name__ == "__main__":
    main()
