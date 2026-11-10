# 대화 압축 기록

대화가 압축될 때마다 요약이 자동으로 쌓인다.

## 2026-11-09 22:40 (자동 압축, 세션 550c27d0)

<analysis>
This summary continues the Side A Android app session. Below is everything since the previous summary, in order.

1. **Commit request** ("작업 트리 변경 사항을 적절한 메시지와 함께 커밋하세요"), with mid-turn requests folded in:
   - **Remove track numbers** in the app and in Figma.
   - **Pull behavior:** at the top of the album, only the tracklist should react to a downward pull; the mini bar must stay fixed.
   - **Spotify reference:** compare against Spotify's pull at the top and at the bottom.
   - What was done:
     - Removed the `.no` column from the template.
     - Removed the '번호' frame from the Figma '트랙 줄' component set (117:45).
     - Turned off WebView overscroll in MainActivity.
     - Added a JS stretch that scales `#tracks` with scaleY, from the top or bottom edge depending on which end is pulled.
     - Added large and generated outputs to `.gitignore`. The audio folder is 1.3GB, so it was ignored.
   - Committed 2c23c8d. Nothing pushed.

2. **Splash animation (all verified on the phone):**
   - The 9 ellipses enter from the right, leftmost first, and settle into place.
   - Second sequence added: a wave, then a zoom-out fade.
   - Slowed down after "너무 빨리 지나가는느낌이야".
   - The native splash icon is now blank, and `launchShowDuration` is 0.

3. **Lyrics top fade:** it no longer covers the first line. The top fade only applies once the lyrics have scrolled (`.lyr.down`).

4. **App icon:**
   - Logo enlarged by re-rendering it from the Figma ellipse geometry.
   - User: "상하 여백 맞춰". Logo height set to 0.651 and moved down by 3/158. Measured margins: L29 R30 T25 B25.

5. **Settings vs Figma:**
   - User asked why Downloads was missing, so Account and Downloads were restored per Figma.
   - Removed the license line, and removed licenses from the Voice credits toast.
   - Slider requested, then clarified: the slider goes inside the bottom sheet, not directly on the Settings screen.
   - Push notifications section added under Account.
   - Figma updated: a Notifications section was added to frames 07, 07b and 08. Changing sheet 08 to a slider is still pending.

6. **Answers given:**
   - Bundled audio in the app is 19MB.
   - Korean spacing: "I'm은" (particle attached) is correct.

7. **Latest message:** put an album-wide download button at the right end of the album header, and record it in the policy docs. No auto-download on play. Placement only for now.
   - Nuance: playback currently pre-fetches the next episode (`warmNext`) on the web. The user says no auto-download on play, so that should probably be disabled. The "Download next episode" setting default may need to be off too, or reconsidered.

Pending: the Figma 08 slider sheet, docs updates, Figma placement of the download button, and possibly a commit (only if asked).
</analysis>

<summary>
1. Primary Request and Intent:
   - **Earlier standing goals:**
     - Finish the Side A Android app (Capacitor) autonomously, except server backup/login.
     - Answer in Korean, plain 해요체. Never commit unless asked. Confirm paid costs first.
     - Keep the existing design when editing; use Lucide icons. Record decisions in the spec and plan docs. Keep Figma in sync with the app.
     - SECURITY: the signing key lives in learn-english/signing/ (gitignored) and must never be committed. Never print the keystore password in chat.
   - **This segment's requests, in order:**
     1. Commit the working tree. Done: 2c23c8d, nothing pushed.
     2. Remove track numbers from album tracklists, in the app and in Figma. Done.
     3. At the top of the album, a pull should move only the tracklist; the mini bar stays fixed. Match Spotify's pull at the top and the bottom. Done.
     4. Splash: the 9 vector pieces enter right-to-left, leftmost first, and gather in place. Then add one more sequence. Then make it slower. Done.
     5. The first lyric line must not be covered by the top fade. Done.
     6. The app icon logo was too small, then the top/bottom margins should match. Done: margins L29 R30 T25 B25.
     7. Settings must match Figma/policy (Downloads was missing). Remove the font license line at the bottom. Done.
     8. Lyrics size as a slider inside the bottom sheet (not on the Settings screen), no real-size preview. Add a Push notifications item in a section under Account. App done; Figma partly done.
     9. **LATEST:** "앨범 트랙리스트 상단 헤더 우측 끝 액션버튼에 다운로드 버튼을 배치하자, 이게 앨범 전체 다운로드 버튼, 그리고 플레이시 자동 다운로드는 하지마, 일단 배치만 해놔 정책이랑. 아직 클라우드플레이어ㅔ 연결은 안했고 강제로 앱에 사운드파일을 넣어두긴햇지만 하긴해야해"
   - **Questions answered:**
     - Real bundled audio is 38 files, 19MB (APK 22MB). The 1.3GB is the raw work folder (spikes/episode-01/audio: season 821M, beginner2 454M, 5,400 wav).
     - "I'm은" with the particle attached is correct Korean spacing.

2. Key Technical Concepts:
   - Capacitor 8 Android wrapper.
   - **Build chain:**
     - `cd spikes/episode-01 && python build_page.py && python build_pwa.py`
     - `cd side-a && node scripts/copy-web.mjs && npx cap sync android`
     - `cd android && JAVA_HOME="C:/Program Files/Android/Android Studio/jbr" ./gradlew.bat assembleRelease -q`
     - `adb install -r app/build/outputs/apk/release/app-release.apk`
   - **Line endings:** template.html is CRLF. Python edits must read bytes, normalize, and write back with `\r\n`.
   - **Overscroll:** `setOverScrollMode(View.OVER_SCROLL_NEVER)` disables the WebView stretch. A JS scaleY stretch on `#tracks` replaces it.
   - **Adaptive icon:** `inset 16.7%` foreground and background. Foreground PNGs are rendered at the visible size (ldpi 54 … xxxhdpi 288).
   - **Splash:** the native splash is plain black. The animation runs in the page as `.intro`.
   - **Phone handling:**
     - The phone's screen timeout must be restored to 60000 after testing; 1800000 is used during tests.
     - Git Bash rewrites `/sdcard` paths, so use PowerShell for screenrecord.
     - The app drawer opens by swiping up from home.
   - **Figma:** file key `31ndvuyn7Zkf4sScTUgvjq`, single page '와이어프레임'.

3. Files and Code Sections:
   - **`spikes/episode-01/app/template.html`** (main UI)
     - **Track rows:**
       - Number span removed; `.trk-go` grid is now `minmax(0,1fr) auto`.
       - `trackRow(i, n)` inner is now `<span class="tt"><b>…</b></span><span class="tm">…</span>`.
       - The playing row is shown only by a green title (`.trk.on b`).
     - **Pull stretch** (inserted before `let exitAsk = 0;`). It acts on `$('vAlbum')` and `$('tracks')`:
       - `atTop()` / `atEnd()` decide which edge is being pulled.
       - Scale is `1 + .06*(1-Math.exp(-|dy|/400))`.
       - Transform origin is `50% 0` at the top and `50% 100%` at the bottom.
       - Release transition: `.35s cubic-bezier(.2,.8,.2,1)`.
       - touchmove is non-passive and calls preventDefault.
     - **Intro (splash):**
       - Placement: `<div class="intro" id="intro" aria-hidden="true"><svg viewBox="130 337 100 106">` with 9 ellipses with `style="--i:k"`, placed right before `<div class="app">`.
       - Ellipse geometry (x, y, w, h in Figma coordinates):
         - (130.02,374.18,3.36,32.76)
         - (137.72,358.08,5.88,64.96)
         - (147.24,347.3,9.8,85.26)
         - (158.86,341.28,12.6,97.44)
         - (172.86,337.78,14.14,104.44)
         - (188.54,341.28,12.46,97.44)
         - (202.96,347.3,9.66,85.26)
         - (216.4,358.08,5.74,64.96)
         - (226.62,374.32,3.36,32.48)
       - Fill: #1ac457.
       - CSS:
         - `.intro ellipse { transform-box: fill-box; transform-origin: 50% 50%; animation: introIn 1s cubic-bezier(.16,1,.3,1) calc(var(--i)*110ms) both, introWave .7s ease-in-out calc(2.2s + var(--i)*70ms) }`
         - `@keyframes introIn { from { transform: translateX(240px); opacity: 0 } 40% { opacity: 1 } to { transform: none; opacity: 1 } }`
         - `@keyframes introWave { 0%,100% { transform: none } 45% { transform: scaleY(1.35) } }`
         - `.intro.out` fades opacity over .5s, and the svg scales to 1.25 over .5s.
       - JS: before `const icons =`, `setTimeout(() => { $('intro').classList.add('out'); setTimeout(() => el.remove(), 520) }, reducedMotion ? 400 : 3700)`.
     - **Lyrics fade:**
       - `.lyr` uses `--ft: 0px` in its mask gradient; `.lyr.down { --ft: 24px }`.
       - `$('script').addEventListener('scroll', e => e.target.classList.toggle('down', e.target.scrollTop > 4), { passive: true });`
     - **Settings view `#vSettings`** (current order):
       - **Account:**
         - `<button class="row two" data-signin>` containing `<span class="row-t"><b>Sign in</b><small>Save your listening history with Google</small></span>` and a chevron.
         - Description text: "Sign in to keep where you left off and how much you listened, even after reinstalling the app or changing phones."
         - Sign in shows the toast 'Sign-in is coming in a later update.'
       - **Notifications:**
         - Row "Push notifications" with switch `data-push`.
         - Description text: "Get a heads-up when new episodes are added."
       - **Playback:**
         - `<button class="row" data-sheet="size">` "Lyrics text size", showing `#sizeVal` and a chevron.
         - Korean translation switch.
         - Existing description text.
       - **Downloads:**
         - "Download next episode" switch `data-dl`.
         - "Wi-Fi only" switch `data-wifi`.
         - "Storage used" with `#storeVal`.
         - `<button class="row" data-deldl><b class="danger-t">Delete downloads</b>`.
         - Description text: "Episodes you play and the next one are saved on this phone, so they play without internet."
       - **About:**
         - Version 1.0.0.
         - `<button class="row" data-credits>` Voice credits with a chevron; shows the toast 'Voices by ElevenLabs.'
         - The license line is removed.
     - **CSS added:**
       - `.row.two`, `.row > .row-t {display:block;…}` (needed to override the `.row > span` flex rule), `.row-t b/small`, `.row > b.danger-t`.
       - `.sz-box`, `.sz-lab`, `.sz-lab span.on`.
       - `.range` slider styles: track 4px, white 20%, filled `var(--hi)` up to `--p`, thumb a 20px white circle.
       - `.opt.sz` was removed.
     - **Size sheet `#shSize`:** contains `<div class="sz-box"><input type="range" class="range" id="sizeRange" min="0" max="2" step="1"><div class="sz-lab" id="sizeLab"><span>Default</span><span>Large</span><span>Extra large</span></div></div>`.
     - **JS:**
       - `S` defaults now include `dl: true, wifi: false, push: true`, and `store.set` saves dl, wifi, push.
       - `syncRange()` sets the value, sets `--p`, and toggles `.on` on the label.
       - `renderSize() { syncRange() }`.
       - `$('sizeRange').addEventListener('input', e => setSize(+e.target.value))`.
       - `setSize` calls `syncRange()`.
       - `renderSettings` calls syncKo and syncDl.
       - Settings route: `if (base === 'settings') { renderSettings(); showStorage(); }`.
       - `syncDl()` syncs the dl, wifi and push switches.
       - `const BUNDLED_MB = +'__BUNDLED_MB__' || 0;`
       - `showStorage()`: on native shows BUNDLED_MB, on web shows `navigator.storage.estimate().usage`, formatted with toFixed(1).
       - `deleteDownloads()`: on native shows the toast 'Episodes are built into the app, so there is nothing to delete.'; on web deletes the `audio*` caches and shows 'Downloads deleted.'
       - `warmNext()` now returns if `CAP || !S.dl`, or if wifi-only is on and the connection type is not wifi/ethernet.
       - The `[data-size]` click handler was removed.
   - **`spikes/episode-01/build_pwa.py`:** before writing index.html, `body = body.replace("__BUNDLED_MB__", f"{sum(f.stat().st_size for f in files)/1048576:.1f}")`. The value is currently 15.6.
   - **`side-a/android/app/src/main/java/com/seongbeom/sidea/MainActivity.java`:** added `import android.view.View;` and `getBridge().getWebView().setOverScrollMode(View.OVER_SCROLL_NEVER);` after setLoadWithOverviewMode.
   - **`side-a/capacitor.config.json`:** `SplashScreen.launchShowDuration` = 0.
   - **`side-a/android/app/src/main/res/drawable/splash_blank.xml`** (new): transparent shape. styles.xml `windowSplashScreenAnimatedIcon` = `@drawable/splash_blank`.
   - **Icon files:** `mipmap-*/ic_launcher_foreground.png`, `ic_launcher.png`, `ic_launcher_round.png`, `assets/icon-foreground.png` and `assets/icon-only.png` re-rendered with PIL. F = .68*100/104.44 ≈ .651; foreground offset DY = 3/158.
   - **`.gitignore`:** added `__pycache__/`, `spikes/episode-01/audio/`, `spikes/episode-01/web/`, and `spikes/episode-01/app/*.webm`, `*.mp3`, `*.len`, `spikes/episode-01/app/episode-01.html`.
   - **Docs:**
     - **Spec** (`docs/superpowers/specs/2026-11-07-story-audio-english-design.md`):
       - Track row line updated: no number.
       - Sub type usage no longer mentions numbers.
       - Splash animation described in '11 시작 화면'.
     - **Plan** (`docs/superpowers/plans/2026-11-09-side-a-android-app.md`):
       - Added "### 2~4단계 뒤 고친 것 (2026-11-09 밤)" covering track numbers, pull behavior, splash animation, lyric fade and icon size.
       - Not yet updated for the settings restore, notifications, slider sheet, license removal, icon centering, or the download button.
       - Line 59 still says Downloads/Account were hidden and a license line was added, which is now outdated.
       - Line 85 still says licenses are shown in the app.
       - Spec lines 518-531 (Playback "누르면 고르는 시트", 08 sheet description, 알림 지금 넣지 않는다) need updating.
   - **Figma:**
     - Track row component set 117:45: the '번호' child was removed from all variants.
     - Notifications section added (cloned from Downloads) in 07 (220:759 → section 266:1712), 07b (249:1633 → 266:1737) and 08 background (249:1724 → 266:1762). Frames grew by 120.
     - 08 size sheet (249:1812) still shows the 3 option rows (Default/Large/Extra large at real size). It needs converting to a slider plus labels.

4. Errors and fixes:
   - **CRLF converted to LF** by a Python text-mode write, which doubled the diff. Fixed by rewriting with CRLF; edits now go through bytes.
   - **`<body` not found** in the template (no body tag). Inserted before `<div class="app">` instead.
   - **Bash rewrote `/sdcard`** into a Git path for screenrecord. Used PowerShell instead.
   - **Wrong `du` total:** the untracked size was first reported as about 41MB because of an xargs mistake. The real audio folder is 1.3GB, so it was gitignored instead of committed.
   - **Sign-in row not two-line:** the `.row > span` flex rule overrode it. Fixed with the `.row > .row-t` override.
   - **Storage showed "16 MB":** changed to always use toFixed(1).
   - **Slider placement:** I first put the slider directly on Settings. The user clarified it belongs inside the bottom sheet, so it was moved.
   - **"상하 여백 맞춰":** first interpreted as matching top/bottom to left/right, so the logo was resized. Then I measured top 22 vs bottom 28 and shifted the logo down; now 25/25.
   - **Icon page search:** home screen swipes did not change pages; the app drawer opens by swiping up.
   - **Phone use:** I assumed the user was using the phone; the user said "아냐 폰 안써 확인해", so I continued checking on the phone.

5. Problem Solving:
   - Verified on the phone with screenshots and recordings:
     - Pull stretch at the top and bottom matches Spotify.
     - Splash sequence (intro.mp4 and intro2.mp4 were sent to the user).
     - Lyric first line is clear.
     - Icon margins.
     - Settings layout and the slider sheet.
   - The phone's screen timeout was restored to 60000 after the settings check, but the last test raised it to 1800000 again. It must be restored.

6. All user messages (this segment):
   - "작업 트리 변경 사항을 적절한 메시지와 함께 커밋하세요."
   - "글고 앨범 트랙리스트에서 앞에 트랙넘버는 전부 빼줘, 피그마도 같이 반영"
   - "그리고 앨범트랙리스트에서 최상단인상태에서 손가락으로 아래로 당기면 트랙리스트만 반응하고 그외에는 안움직이게 해줘 미니 바까지같이 흔들려서 이건 고정으로해야해ㅔ"
   - "내 폰의 스포티파이를 열어서 같은 환경으로 스크롤해서 뭐가 움직이고 뭐가 반응안하는지를 봐ㅘ"
   - "화면을 최하단으로 내렸을때 인터렉션도확ㅇ니해 스포티파이에서"
   - "그리고 앱 스플래시화면 안에 로고가 지금 다 벡터로 그렸으니까 이런 애니메이션 되는지 한번 해보자 / 총 9조각이잖아, 이제 이게 제일 좌측쉐잎부터 우에서 좌로 등장해서 지금의ㅏ 자리로 모이는 애니메이션"
   - "소리가 1.3기가나됨? 이거 원래 소리 압축 규칙있던걸로 아는데 그래도 이정도양이야? 실제 앱빌드에 들어간 파일만따졌을때"
   - "좋아 그렇게 등장하고 뭔가 그다음 시퀀스가 하나 더 있엇음 좋겠어"
   - "너무 빨리 지나가는느낌이야"
   - "트랙하나 플레이하고 가사창 보면 제일 첫 라인 윗쪽이 약간의 페이드 딤 처리에 가려졌어. 가장 첫 라인은 이 효과 제외하자"
   - "좋아, 그리고 앱 아이콘 실제적용된거보니까 까만배경안에 이 아이콘이 너무 작게 들어갔어"
   - "그리고 이 띄어쓰기 이게 맞아 i'm은 이 맞아 i'm 은 이 맞아?"
   - "앱 아이콘이 뭔가 세이프안에 중앙에 위치한게 아닌듯한 느낌이야"
   - "상하좌우 내부 패딩이 미묘하게 차이가나"
   - "상하 여백 맞춰"
   - "그리고 앱 설정이 왜 피그마랑 규칙에서 정한 것과 개발된버전이 달라? 다운로드관련이 없어"
   - "아냐 폰 안써 확인해"
   - "그리고 설정 맨 하단 폰트에 대한 라이센스 정보 빼"
   - "그리고 설정에서 가사 글자크기 셋팅 슬라이더로 해줘"
   - "실제글자크기로 ㅂ프리뷰는 하지마"
   - "푸시알림 설정이 빠져있네, 처음에 권한은 받아서 있을줄알았는데 일단 계정 아래 섹션으로 푸시알림 항목 넣어주고, 가사 크기 슬라이더를 바텀시트 안에 해달라는거야. 설정에바로하는게 아니라"
   - "앨범 트랙리스트 상단 헤더 우측 끝 액션버튼에 다운로드 버튼을 배치하자, 이게 앨범 전체 다운로드 버튼, 그리고 플레이시 자동 다운로드는 하지마, 일단 배치만 해놔 정책이랑. 아직 클라우드플레이어ㅔ 연결은 안했고 강제로 앱에 사운드파일을 넣어두긴햇지만 하긴해야해"

7. Pending Tasks:
   - **Album download button (latest request):**
     - Add an album-wide download button (Lucide, e.g. arrow-down-to-line or download) at the right end of the album screen header (`#vAlbum header.bar`, which currently has only a back button on the left).
     - It is placement only: since audio is bundled and R2 is not connected yet, tapping it should show a toast or be a placeholder.
     - Stop auto-download on play: disable `warmNext` pre-fetching, and reconsider the "Download next episode" default and description accordingly.
     - Record the policy in the spec and plan: album download button, no auto-download on play, R2 connection still to do.
     - Mirror the button in the Figma album frame '02 앨범 (전체 스크롤)' (119:55).
   - **Figma 08 sheet:** convert the size sheet (249:1812) from 3 real-size option rows to a slider plus small labels Default / Large / Extra large, matching the app.
   - **Docs:** update for the settings restore (Account, Downloads), the Notifications section, the slider in the bottom sheet, license line removal (fix plan lines 59 and 85), icon centering, and the outdated spec lines 518-531 ("알림은 지금 넣지 않는다", sheet description).
   - **Phone:** restore the screen timeout with `adb shell settings put system screen_off_timeout 60000`.
   - **Commit:** do not commit unless asked. Never commit signing/. Push is still not done.

8. Current Work:
   - Just finished the app side of the notifications and slider-sheet change, verified on the phone.
   - Ran a Figma script that added the Notifications section to frames 07, 07b and 08. Result: sections 266:1712, 266:1737, 266:1762; frames grew by 120.
   - Then the user sent the latest request about the album-wide download button.
   - Remaining at this point: the Figma 08 slider conversion, docs updates, and the new download button work.

9. Optional Next Step:
   - Implement the latest request: "앨범 트랙리스트 상단 헤더 우측 끝 액션버튼에 다운로드 버튼을 배치하자, 이게 앨범 전체 다운로드 버튼, 그리고 플레이시 자동 다운로드는 하지마, 일단 배치만 해놔 정책이랑."
     - Add the download icon button to the right end of the `#vAlbum` header in template.html, with a placeholder action.
     - Remove auto pre-download on play (`warmNext`).
     - Record the policy in the spec and plan docs.
     - Mirror it in the Figma album frame.
     - Rebuild, install, and verify on the phone.
   - Then finish the Figma 08 slider sheet and the docs updates. Restore the phone's screen timeout to 60000 at the end.
</summary>

## 2026-11-10 14:04 (자동 압축, 세션 c746a846)

<analysis>
Chronological recap of this segment:
- Continued the Speak Up voice generation: 70 calls across ep1–10, session ids recorded in the scratchpad file su-sessions.txt. Total cost 2,919 credits.
- User mid-turn: "그리고 피그마에 쉐도우용 앨범커버만들어둠. 같이 앱에 적용해". Found the Figma file 31ndvuyn7Zkf4sScTUgvjq with frames cover_쉐도잉1–7. Downloaded them at 2x (720px), converted to WebP as app/cover-sh1..6.webp (7 is reserved for the profanity album) and pulled colors from them. Updated SHADOWS in template.html (c and art), added the Speak Up entry and KO_TITLE.
- User mid-turn: Play all on each home section. Implemented with secQ, secList, inAlbum and the shelf-h header. Tested in the browser: 50 tracks, playback crosses albums.
- The background agent downloaded all 70 clips and they verified fine. Built the 10 Speak Up tracks (s6-01..10, 83.7–104s, ~16 min). Ran build_page and build_pwa (148 audio), built the APK and installed it.
- User: show speaker names in shadowing lyrics, e.g. "Jane : …" / "Me : …". Implemented the `.who` label. User then: "이름은 니가 정한 이름으로 넣어 나 말고 다른 캐릭터들". Added a SHADOW_WHO map of names per episode.
- User: "이제 따라해보세요 는 화자 표시 필요없어". Excluded the repeat section, then also restricted labels to the Me/Partner speakers so Guide lines like "One more time." get none. Browser check passes.
- The spec was updated for covers, Play all, Speak Up, the profanity test, and speaker labels. But the spec labels bullet still says Jane for all; it needs updating to per-episode names and to no labels in the repeat section and on guide lines.
- The latest changes (per-episode names, repeat exclusion, Guide exclusion) are NOT yet in an APK or installed on the phone. The final report is pending.
</analysis>

<summary>
1. Primary Request and Intent:
   - **Album ⑥ "Speak Up" (항의와 언쟁):** the user approved the script with "이대로 만들어". It is now voiced, built, registered and installed (first install).
   - **Figma shadowing covers:** apply the covers the user made in Figma to the app ("피그마에 쉐도우용 앨범커버만들어둠. 같이 앱에 적용해"). Done.
   - **Play all:** add Play all at the right end of each home section header. It plays all tracks of that section in order. Done.
   - **Speaker labels in shadowing lyrics:** show who is speaking (e.g. "Jane : …", "Me : …").
     - Follow-up: partner names are mine to choose per character ("나 말고 다른 캐릭터들").
     - Follow-up: no speaker label in the "이제 따라해보세요" (repeat) part.
   - **Standing constraints:**
     - Reply in Korean 해요체.
     - Paid API: disclose cost and get consent first, and never re-call a generation that has started.
     - Record decisions and changes in `docs/superpowers/specs/2026-11-07-story-audio-english-design.md` and search for old wording.
     - Never commit `signing/`. Commit only when asked; nothing is committed yet.
     - Use Lucide for icons and keep existing designs.
     - Review scripts before making voices.
   - **Earlier pending:** the user hasn't said whether the profanity test audio sounds clear. The profanity album ⑦ comes later. Rule: no slurs (racial, gender or orientation).

2. Key Technical Concepts:
   - **ElevenLabs connector** (`mcp__67a9ac48…creative_generate_speech`):
     - flow `jnVnLb7w5iKgPNv7CQXU`, model `eleven_v4`
     - voices: A (male, "Me") `7EzWGsX10sAS4c9m9cPf`; B (female, Partner) `OYTbf65OHHFELVut7v2H`
     - tags `[casual]`, `[annoyed]`, `[firm]`
   - **Clip downloads** are delegated to a background agent that must not generate anything.
   - **Figma:**
     - MCP `mcp__d8583ef6…`: `use_figma` for reads, `download_assets` (png, scale 2) for exports.
     - File key `31ndvuyn7Zkf4sScTUgvjq`, page 와이어프레임.
     - Covers: cover_쉐도잉1 `285:2079`, 2 `285:2099`, 3 `285:2089`, 4 `285:2023`, 5 `285:2077`, 6 `285:2083`, 7 `285:2091`.
   - **WebP conversion:** PIL, quality 80. Use Windows paths (`D:/...`) in Python, not `/d/...`.
   - **Build:**
     ```
     cd spikes/episode-01; export PYTHONIOENCODING=utf-8
     python build_shadowing.py speak-up N
     python build_page.py; python build_pwa.py
     ```
   - **APK and install:**
     ```
     cd D:/project/learn-english/side-a && node scripts/copy-web.mjs && npx cap sync android && cd android && JAVA_HOME="C:/Program Files/Android/Android Studio/jbr" ./gradlew.bat assembleRelease -q && adb -s 192.168.35.135:46857 install -r app/build/outputs/apk/release/app-release.apk
     ```
     Launch with `adb shell am start -n com.seongbeom.sidea/.MainActivity`.
   - **Browser preview:** `story-pwa` on port 8765 (serves `spikes/episode-01/web`). The service worker caches old builds, so unregister it and clear caches, then reload.

3. Files and Code Sections:
   - **`spikes/episode-01/app/template.html`** (main edits):
     - SHADOWS entries now have new colors and covers:

       | Album | Color | Cover |
       |---|---|---|
       | 스몰토크 | `#a50110` | sh1 |
       | 하루 일과 | `#0c0c0c` | sh2 |
       | 나를 소개하기 | `#013195` | sh3 |
       | 사람 사이 기술 | `#e55317` | sh4 |
       | 식당과 카페 | `#f02778` | sh5 |
       | 항의와 언쟁 | `#4a0379` | sh6 |

     - New entry: `{ name: '항의와 언쟁', en: 'Speak Up', mark: 'UP', about: 'Complain, push back, argue, and make up', c: '#4a0379', art: 'sh6', pats: [10 titles] }`.
     - KO_TITLE gained the 10 Speak Up Korean titles (145 keys total).
     - SHADOW_WHO, inserted before `/* 화의 한국어 제목.`:
       ```
       const SHADOW_WHO = {
         '스몰토크': ['Sarah','Jessica','Rachel','Linda','Amy','Olivia','Rachel','Kate','Sophie','Jessica'],
         '하루 일과': ['Amy','Lauren','Diane','Amy','Rachel','Megan','Megan','Mia','Jessica','Jessica'],
         '나를 소개하기': ['Emma','Zoe','Lena','Grace','Jessica','Natalie','Ashley','Hannah','Sophie','Claire'],
         '사람 사이 기술': ['Amy','Rachel','Megan','Jessica','Jessica','Laura','Olivia','Jessica','Sienna','Sienna'],
         '식당과 카페': ['Zoe','Ivy','Tina','Tina','Tina','Rosa','Nicole','Nicole','Nicole','Jessica'],
         '항의와 언쟁': ['Brittany','Kelsey','Paula','Tiffany','Vanessa','Erin','Chloe','Chloe','Chloe','Chloe'] };
       ```
     - In `lineHtml`, before the final return:
       ```
       if (albumOf(E.course).shadow && (l.speaker === 'Me' || l.speaker === 'Partner') && l.section !== 'repeat') t = `<span class="who">${l.speaker === 'Me' ? 'Me' : (SHADOW_WHO[E.course] || [])[E.n - 1] || 'Partner'}:</span> ${t}`;
       ```
       CSS: `.ln .who { opacity: .6 }`.
     - Play all CSS:
       ```
       .shelf-h { display:flex; align-items:baseline; justify-content:space-between; gap:12px; padding-bottom:12px }
       .shelf h2 { font: var(--t-title); letter-spacing: -.02em }
       .play-all { font: var(--t-head); color: rgb(255 255 255 / .7); padding: 6px 0 6px 12px; margin-block: -6px }
       ```
     - `renderHome` header: `<div class="shelf-h"><h2>${title}</h2>${secList(list).length ? <button class="play-all" data-playall="${SHELVES.findIndex(x => x[1] === list)}">Play all</button> : ''}</div>`.
     - Queue logic replaced sibs:
       ```
       const inAlbum = name => SCRIPTS.map((e,i)=>i).filter(i => has(i) && SCRIPTS[i].course === name).sort((a,b)=> SCRIPTS[a].n - SCRIPTS[b].n || !!SCRIPTS[a].alt - !!SCRIPTS[b].alt);
       let secQ = null;
       const secList = list => list.flatMap(al => inAlbum(al.name).filter(i => !SCRIPTS[i].alt));
       const sibs = () => secQ && secQ.includes(cur) ? secQ : inAlbum(E.course);
       ```
     - Click handler: `[data-playall]` sets `secQ = secList(SHELVES[k][1])` and calls `startEp(secQ[0])`. Tapping a track outside the queue sets `secQ = null`. albumPlay clears secQ unless the same album is already playing.
   - **`spikes/episode-01/build_shadowing.py`:**
     ```
     TAG = {..., "eating-out": "s5", "speak-up": "s6"}
     ```
   - **`spikes/episode-01/build_page.py`:** the shadows dict now includes `"speak-up": "항의와 언쟁"`. Covers glob `app/cover-*.webp`.
   - **`spikes/episode-01/app/cover-sh1..6.webp`** are new files (6–8 KB each). The 7th export (s7, green) is in `E:/Temp/claude/12f846cde673f19c/c746a846-390f-44b9-a261-a4d6c9c43e7d/scratchpad/covers/sh7.webp`, kept for the profanity album.
   - **`spikes/episode-01/audio/shadowing/speak-up/ep01..10/`:** clips d1–d7 plus g1/g2, and s6-NN.webm with timeline.json. Timeline speakers are "Partner", "Me" and "Guide". Sections are talk, repeat and replay.
   - **Spec `docs/superpowers/specs/2026-11-07-story-audio-english-design.md`:**
     - Old "(표지 글자 ME/YOU/EAT…)" mentions were marked 옛, now Figma covers.
     - Added bullets after "이것으로 첫 앨범 5개가 모두 나왔다.":
       - 쉐도잉 앨범 커버
       - 홈 섹션 Play all
       - 항의와 언쟁(Speak Up) 10화 완성 (2,919 credits, 1:24–1:44 per track, ~16 min, s6, cover_쉐도잉6 #4a0379)
       - 욕 음성 시험 (355 credits)
       - 쉐도잉 가사에 말하는 사람
     - The last bullet is OUTDATED: it says Jane for every album. It must change to per-episode names (SHADOW_WHO) and say labels are not shown in the repeat section or on Guide lines.

4. Errors and fixes:
   - **WebP save path:** PIL failed with FileNotFoundError on `/d/...` paths. Fixed by using `D:/...`.
   - **Stale browser build:** the preview showed the old build from the service worker cache. Fixed by unregistering it and clearing caches.
   - **innerText empty:** JS checks on hidden views returned empty `innerText`. Used `textContent` instead.
   - **Guide line labeled:** "One more time." got a partner name. Fixed by labeling only the Me and Partner speakers.
   - **User feedback:** names should be my own choices per character, not Jane for all. The repeat section should have no labels.

5. Problem Solving:
   - Play all was verified in the browser: Shadowing has 50 queued tracks, and ep10 of 스몰토크 is followed by 하루 일과 1.
   - Labels were verified: Emma for About Me ep1 and Chloe for Speak Up ep7. The repeat section and Guide lines have no label.

6. All user messages:
   - "이대로 만들어" (Speak Up script approval, before this segment)
   - "그리고 피그마에 쉐도우용 앨범커버만들어둠. 같이 앱에 적용해"
   - "그리고 각 홈 각 섹션 우측 끝에 Play all 넣어줘, 그럼 이걸 누르면 해당 섹션의 트랙을 전부 순차적으로 듣는 기능이되는거야."
   - "아 그리고 쉐도잉에서 대화예제에서 내가 보는 화면에는 화자가 누군지는 적어줘 Jane : 어쩌고 저쩌고 Me : 어쩌고 저쩌고 이렇게"
   - "이름은 니가 정한 이름으로 넣어 나 말고 다른 캐릭터들"
   - "이제 따라해보세요 는 화자 표시 필요없어"

7. Pending Tasks:
   1. Rebuild the APK with the latest template (per-episode names, no labels in repeat or on Guide lines) and install it on the phone. The web/PWA build is already up to date.
   2. Update the spec's speaker-label bullet: names per episode from SHADOW_WHO, chosen by me (`작성자 판단`), with no labels in the repeat section or on Guide lines. Replace the Jane wording.
   3. Report to the user in Korean:
      - Speak Up is done (2,919 credits, ~16 min).
      - Figma covers are applied; cover 7 (green) is reserved for the profanity album.
      - Play all is added.
      - Speaker labels are added, with the names chosen.
   4. Call `wrap_up`.
   5. Later: the profanity album ⑦, after the user confirms the test audio. Don't commit unless asked.

8. Current Work:
   - Just finished the user's latest request: "이제 따라해보세요 는 화자 표시 필요없어". The template condition now excludes `l.section === 'repeat'` and labels only the 'Me' and 'Partner' speakers. Ran build_page and build_pwa (148 audio).
   - The browser check of Speak Up ep7 showed: "Chloe: Sorry, I can't make it tonight.", "Me: Seriously? You always do this.", …, "Now, repeat after me.", "One more time." (no label), and replay lines labeled.
   - The phone still has the earlier APK, which uses Jane labels everywhere.

9. Optional Next Step:
   - Rebuild and install the APK so the phone has the per-episode names and no labels in the repeat part:
     ```
     cd D:/project/learn-english/side-a && node scripts/copy-web.mjs && npx cap sync android && cd android && JAVA_HOME="C:/Program Files/Android/Android Studio/jbr" ./gradlew.bat assembleRelease -q && adb -s 192.168.35.135:46857 install -r app/build/outputs/apk/release/app-release.apk
     ```
   - Then fix the spec's "쉐도잉 가사에 말하는 사람" bullet to match "이름은 니가 정한 이름으로 넣어 나 말고 다른 캐릭터들" and "이제 따라해보세요 는 화자 표시 필요없어".
   - Then send the wrap_up and the Korean report.
</summary>
