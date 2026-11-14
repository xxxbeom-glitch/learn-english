"""폰에 설치하는 웹앱 폴더(web/)를 만든다.

app/episode-01.html(아티팩트용 본문)을 그대로 감싸서 index.html로 두고,
설치 설정(manifest), 오프라인 저장(sw.js), 아이콘, 음성(b1-NN.webm, r1-NN.webm)을 함께 넣는다.
먼저 build_page.py로 app/episode-01.html을 만든 뒤 실행한다.
"""
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from data_pack import DATA_URL, pack
from game_tips import apply as apply_tips
from game_names import apply as apply_names

HERE = Path(__file__).parent
APP = HERE / "app"
WEB = HERE / "web"
BG, INK = "#5F6B4E", "#F6F3EC"  # 앱 색(--accent, --accent-ink)
# 소리는 앱 안에 넣지 않고 Cloudflare R2(side-a-audio 통)에서 받는다. 올리기는 upload_r2.py(2026-11-10 성범 요청)
AUDIO_BASE = "https://pub-54e325ce90af4f1bad3644fc22432096.r2.dev/audio/"

HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
<script>
/* 폰에서는 화면 폭을 시안과 같은 360으로 잡아, 폭이 넓은 폰에서도 시안 비율 그대로 꽉 차게 키운다.
   두 손가락 확대와 두 번 눌러 확대는 막는다(2026-11-14 성범 지적). 가사는 글자 크기 설정으로 키운다 */
(function () { var m = document.querySelector('meta[name=viewport]');
  function fit() { m.content = (screen.width < 600 ? 'width=360' : 'width=device-width, initial-scale=1') + ', viewport-fit=cover, user-scalable=no' }
  fit(); addEventListener('orientationchange', fit) })();
</script>
<meta name="theme-color" content="#121212">
<meta name="robots" content="noindex">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
</head>
<body>
"""

TAIL = """
<script>
if ('serviceWorker' in navigator) addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
</script>
</body>
</html>
"""

SW = r"""// 이야기 영어 오프라인 저장. 음성은 받아 둔 앨범만 저장본으로 쓰고, 화면 파일은 새 판이 있으면 바꾼다.
const SHELL = 'shell-__VER__', AUDIO = 'audio-v1';
const CORE = ['./', 'index.html', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'PretendardVariable.woff2', 'Outfit-Bold.woff2', 'lucide.min.js', 'sfx-correct.mp3', 'sfx-wrong.mp3', 'game-data.js'];
self.addEventListener('install', e => { e.waitUntil(caches.open(SHELL).then(c => c.addAll(CORE))); self.skipWaiting() });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('shell-') && k !== SHELL).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET') return;
  const url = new URL(r.url);
  if (url.pathname.endsWith('.webm')) { e.respondWith(audio(r)); return }
  if (url.origin !== location.origin && url.pathname.startsWith('/data/')) return;  // R2의 내용 묶음은 앱이 직접 받아 data-v1에 넣는다
  // 화면, 글꼴, 아이콘 라이브러리: 저장본을 먼저 보여 주고 뒤에서 새로 받아 둔다.
  e.respondWith(caches.open(SHELL).then(c => c.match(r, { ignoreSearch: url.origin === location.origin }).then(hit => {
    const net = fetch(r).then(res => { if (res.ok || res.type === 'opaque') c.put(r, res.clone()); return res }).catch(() => hit);
    return hit || net;
  })));
});
// 음성: 받아 둔 앨범(audio-v1)에 있으면 저장본을 쓰고, 없으면 인터넷에서 듣기만 한다.
// 재생할 때 저절로 받아 두지 않는다(2026-11-09 정책). 저장은 앨범 화면의 받기 단추가 맡는다(2026-11-10 연결).
// 건너뛰기용 구간 요청(Range)은 저장본에서 잘라 준다.
async function audio(r) {
  const c = await caches.open(AUDIO), u = new URL(r.url), key = u.pathname + u.search;
  const hit = await c.match(key);
  if (!hit) return fetch(r);
  const range = r.headers.get('range');
  if (!range) return hit;
  const buf = await hit.arrayBuffer(), m = /bytes=(\d*)-(\d*)/.exec(range);
  const start = m && m[1] ? +m[1] : 0, end = m && m[2] ? +m[2] : buf.byteLength - 1;
  return new Response(buf.slice(start, end + 1), { status: 206, headers: {
    'Content-Type': 'audio/webm', 'Content-Length': String(end - start + 1),
    'Content-Range': `bytes ${start}-${end}/${buf.byteLength}`, 'Accept-Ranges': 'bytes' } });
}
"""

MANIFEST = {
    "name": "이야기 영어",
    "short_name": "이야기 영어",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#121212",
    "theme_color": "#121212",
    "lang": "ko",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}


def icon(size, art):
    """Lucide headphones 모양을 앱 색 바탕에 그린다. art는 그림이 차지하는 비율."""
    k = 4  # 크게 그린 뒤 줄여서 가장자리를 부드럽게 한다.
    S = size * k
    im = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(im)
    u = S * art / 24  # Lucide 24칸 격자 한 칸
    o = (S - 24 * u) / 2
    w = round(2 * u)  # 선 두께 2

    def p(x, y):
        return (o + x * u, o + y * u)

    # 머리띠: 중심 (12,12), 반지름 9의 위쪽 반원, 양 끝에서 아래로 이어지는 선
    (x0, y0), (x1, y1) = p(3, 3), p(21, 21)
    d.arc([x0, y0, x1, y1], 180, 360, fill=INK, width=w)
    for x in (3, 21):
        d.line([p(x, 12), p(x, 19)], fill=INK, width=w)
    # 귀 덮개
    for a, b, corners in ((3, 8, (False, True, True, True)), (16, 21, (True, False, True, True))):
        (ax, ay), (bx, by) = p(a, 14), p(b, 21)
        d.rounded_rectangle([ax, ay, bx, by], radius=2 * u, outline=INK, width=w, corners=corners)
    return im.resize((size, size), Image.LANCZOS)


def main():
    apply_tips()  # content/game/tips-*.md의 팁을 app/game-data.js에 넣는다(2026-11-14)
    apply_names()  # 빈칸 고르기에서 뺄 고유명사 목록(2026-11-14)
    # Vercel 연결 정보(.vercel)는 남기고 나머지만 새로 만든다.
    WEB.mkdir(exist_ok=True)
    for f in WEB.iterdir():
        if f.name != ".vercel":
            shutil.rmtree(f) if f.is_dir() else f.unlink()
    body = (APP / "episode-01.html").read_text(encoding="utf-8")
    # 초급(b1-), 팟캐스트(r1-) 음성 가운데 화면이 실제로 쓰는 것만 넣는다(옛 초급 음성은 빠진다).
    files = [f for f in sorted(APP.glob("*.webm")) if f'"{f.name}"' in body]
    # 음성이 다시 만들어지면 주소가 바뀌도록 내용 지문을 붙인다. 폰은 새 주소를 보고 새로 받는다.
    for f in files:
        h = hashlib.sha1(f.read_bytes()).hexdigest()[:8]
        body = body.replace(f'"{f.name}"', f'"{AUDIO_BASE}{f.name}?v={h}"')
    # 설정 · Storage used에 보일, 앱 안에 넣는 소리 크기
    body = body.replace("__BUNDLED_MB__", "0")
    # 전체 소리 크기(2026-11-14 Download all audio를 빼서 화면에는 안 보인다)(화의 소리와 해설 + 문장 게임 소리). 게임 소리는 R2의 audio/game/에 있다(upload_game_r2.py)
    total = sum(f.stat().st_size for f in files) + sum(f.stat().st_size for f in (APP / "game").glob("*.webm"))
    body = body.replace("__ALL_MB__", str(round(total / 1048576)))
    # 내용 묶음(대본·시간표, 게임 문장, 커버)을 data-pack/에 만들고, 그 목록을 이 앱의 기본 복사본 표시로 넣는다.
    # 앱은 켤 때 R2의 목록과 견주어 새 판이면 바뀐 파일만 받는다(2026-11-13 성범 요청). 올리기는 publish_data.py
    mf = pack(body, round(total / 1048576))
    body = body.replace("__MANIFEST__", json.dumps(mf, ensure_ascii=False)).replace("__DATA_URL__", DATA_URL)
    (WEB / "index.html").write_text(HEAD + body + TAIL, encoding="utf-8")
    (WEB / "manifest.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=2), encoding="utf-8")
    # sfx-*.mp3: 문장 게임의 정답·오답 효과음(2026-11-13). 작아서 R2가 아니라 앱 안에 넣는다
    for f in [APP / "PretendardVariable.woff2", APP / "Outfit-Bold.woff2", APP / "lucide.min.js", APP / "sfx-correct.mp3", APP / "sfx-wrong.mp3", APP / "game-data.js"]:
        shutil.copy(f, WEB / f.name)
    ver = hashlib.sha1(body.encode()).hexdigest()[:8]  # 화면이 바뀌면 저장본을 새로 받게 한다.
    (WEB / "sw.js").write_text(SW.replace("__VER__", ver), encoding="utf-8")
    icon(192, 0.62).save(WEB / "icon-192.png")
    icon(512, 0.62).save(WEB / "icon-512.png")
    icon(512, 0.5).save(WEB / "icon-maskable-512.png")
    (WEB / "vercel.json").write_text(json.dumps({"headers": [
        {"source": "/sw.js", "headers": [{"key": "Cache-Control", "value": "no-cache"}]},
        {"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex"}]},
    ]}, indent=2), encoding="utf-8")
    print("내용 판", mf["v"], "(올리기: python publish_data.py)")
    print(len(files), "audio,", sum(f.stat().st_size for f in WEB.iterdir() if f.is_file()) // 1024, "KB")


if __name__ == "__main__":
    main()
