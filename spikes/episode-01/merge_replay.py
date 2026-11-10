"""The Replay의 4부작 화를 한 트랙으로 합친다 (2026-11-10 성범 요청).

python merge_replay.py

대본과 녹음은 화마다 끊기는 것을 전제로 만들었다("Okay, we're back. Last time ..."). 그래서 2~4부 첫머리의
다시 왔다는 말과 지난 이야기 요약, 앞 부 끝과 겹치는 질문을 잘라 내고 이어 붙인다. 새로 녹음하지 않는다.
원본은 화마다 이어 붙인 MP3(uiux-study/sounds/album-0N-part-K.mp3)와 build_podcast.py가 만든 시간표
(audio/podcast/rN-0K.json)다. 결과는 rN-01.json, app/rN-01.webm 하나이고 rN-02~04는 지운다.
한 번 합친 뒤 다시 돌리려면 시간표 원본(rN-0K.json)이 필요하므로, 합치기 전 원본을 audio/podcast/parts/에 옮겨 둔다.
"""
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
POD = HERE / "audio" / "podcast"
PARTS = POD / "parts"
SRC = Path("D:/project/uiux-study/sounds")
APP = HERE / "app"
GAP = 0.4
# 인트로 음악(2026-11-10 성범 요청): 힙합 비트를 앞에 깔고 인사가 시작되면 작게 줄였다가 페이드아웃한다
MUSIC = SRC / "MUSCSmpl-playing_old_samples_-Elevenlabs.mp3"
INTRO = 2.5   # 음악만 나오는 시간. 목소리와 시간표를 이만큼 뒤로 민다
# 음악 파일이 6.7초라 금방 끝났다(2026-11-10 성범: 페이드아웃이 너무 빠르다). 비트를 반복해 깔고 FADE_AT초부터 FADE초 동안 줄인다
FADE_AT, FADE = 11.0, 6.0

# 앨범마다 합친 트랙 제목, 부마다 첫머리에서 버리는 줄 수, 그리고 줄 앞부분만 자르는 경우(부, 자를 초, 새 영어, 새 뜻)
ALBUMS = {
    1: {"title": "Drake vs Kendrick", "drop": {2: 2, 3: 0, 4: 1},
        # 3부 첫 줄 "We're back. So many songs ..."에서 "We're back."만 뺀다 (0.94초 뒤 쉼에서 자름)
        "trim": {3: (0.86, "So many songs in three days. Crazy. But now, I want the gossip. Dana, give me the tea.",
                     "3일 동안 곡이 쏟아졌죠. 미쳤죠. 근데 이제 가십이 듣고 싶어요. 데이나, 썰 좀 풀어 줘요.")}},
    2: {"title": "Young Thug and the YSL Trial", "drop": {2: 2, 3: 2, 4: 1}, "trim": {}},
}


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]))


def main():
    PARTS.mkdir(exist_ok=True)
    for n, cfg in ALBUMS.items():
        for k in range(1, 5):
            f = POD / f"r{n}-{k:02d}.json"
            if f.exists() and not (PARTS / f.name).exists():
                shutil.move(f, PARTS / f.name)
        lines, segs, t = [], [], 0.0
        for k in range(1, 5):
            tl = json.loads((PARTS / f"r{n}-{k:02d}.json").read_text(encoding="utf-8"))
            mp3 = SRC / f"album-{n:02d}-part-{k}.mp3"
            ls = tl["lines"][cfg["drop"].get(k, 0):]
            head = ls[0]["start"]
            if k in cfg["trim"]:
                cut, text, meaning = cfg["trim"][k]
                head = ls[0]["start"] + cut
                ls = [dict(ls[0], text=text, meaning=meaning, start=head)] + ls[1:]
            tail = min(ls[-1]["end"] + 0.05, dur(mp3))
            if segs:
                t += GAP
            for l in ls:
                lines.append(dict(l, start=round(INTRO + t + l["start"] - head, 2), end=round(INTRO + t + l["end"] - head, 2)))
            segs.append((mp3, head, tail))
            t += tail - head
        # 부마다 잘라서 사이에 GAP초 쉼을 두고 잇는다
        args, parts = ["ffmpeg", "-v", "error", "-y"], []
        for i, (mp3, a, b) in enumerate(segs):
            args += ["-i", str(mp3)]
            parts.append(f"[{i}:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=mono[s{i}]")
        sil = f"anullsrc=r=44100:cl=mono,atrim=0:{GAP}"
        chain = ""
        for i in range(len(segs)):
            if i:
                parts.append(f"{sil}[g{i}]")
                chain += f"[g{i}]"
            chain += f"[s{i}]"
        parts.append(f"{chain}concat=n={2 * len(segs) - 1}:v=0:a=1[out]")
        out, wav = APP / f"r{n}-01.webm", POD / f"r{n}-voice.wav"
        subprocess.run(args + ["-filter_complex", ";".join(parts), "-map", "[out]", str(wav)], check=True)
        mix = (f"[0:a]adelay={int(INTRO * 1000)},apad=pad_dur=0[v];"
               f"[1:a]aformat=sample_rates=44100:channel_layouts=mono,"
               f"volume='if(lt(t,{INTRO - 0.3}),0.85,if(lt(t,{INTRO + 0.5}),0.85-(t-{INTRO - 0.3})/0.8*0.65,0.2))':eval=frame,"
               f"afade=t=out:st={FADE_AT}:d={FADE},atrim=0:{FADE_AT + FADE}[m];"
               "[v][m]amix=inputs=2:duration=first:normalize=0[out]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-stream_loop", "3", "-i", str(MUSIC), "-filter_complex", mix,
                        "-map", "[out]", "-c:a", "libopus", "-b:a", "24k", str(out)], check=True)
        wav.unlink()
        total = dur(out)
        tl = {"title": cfg["title"], "duration": round(total, 2),
              "sections": [{"key": "talk", "title": "대화", "start": 0}], "lines": lines}
        (POD / f"r{n}-01.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
        for k in range(2, 5):
            (APP / f"r{n}-{k:02d}.webm").unlink(missing_ok=True)
        print(f"r{n}", cfg["title"], len(lines), "lines, timeline", round(t, 2), "track", round(total, 2))


if __name__ == "__main__":
    main()
