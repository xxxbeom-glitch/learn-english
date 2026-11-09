// 지금 웹 앱(spikes/episode-01/web, build_pwa.py가 만듦)을 앱 안에 넣을 www/로 복사한다.
// 소리 파일도 지금은 앱 안에 넣는다(2026-11-09 성범: 현재는 로컬로 넣어도 됨. 나중에 R2로 옮김).
// 웹 전용 파일(서비스 워커, Vercel 설정, 설치 설정)은 앱에서 필요 없어서 뺀다.
import { cpSync, existsSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = join(root, "..", "spikes", "episode-01", "web");
const out = join(root, "www");
const SKIP = new Set(["sw.js", "vercel.json", "manifest.webmanifest"]);

if (!existsSync(join(src, "index.html"))) {
  console.error("먼저 spikes/episode-01에서 build_page.py와 build_pwa.py를 실행하세요.");
  process.exit(1);
}
rmSync(out, { recursive: true, force: true });
cpSync(src, out, { recursive: true, filter: (p) => !SKIP.has(p.split(/[\\/]/).pop()) });

// 서비스 워커 등록 줄을 지운다. 앱은 파일이 이미 폰 안에 있어서 필요 없다.
const index = join(out, "index.html");
const html = readFileSync(index, "utf8");
const line = /^.*navigator\.serviceWorker\.register.*$\n?/m;
if (!line.test(html)) throw new Error("서비스 워커 등록 줄을 못 찾았어요. build_pwa.py가 바뀌었는지 확인하세요.");
writeFileSync(index, html.replace(line, "").replace(/<link rel="manifest"[^>]*>\n?/, ""));
console.log("www/ 준비 끝:", out);
