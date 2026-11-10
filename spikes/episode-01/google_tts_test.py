"""구글 Gemini TTS 시험 (2026-11-09). 1화 영어 문장 몇 개를 만들어 일레븐랩스 조각과 비교한다. 시험판 코드다.

python google_tts_test.py MODEL  → audio/unused/google-test/MODEL/<id>.mp3
키는 learn-english/.env의 GEMINI_API_KEY에서 읽고, 화면에 찍지 않는다.
"""
import base64
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
CLIPS = HERE / "audio" / "beginner2" / "ep01" / "clips.json"
PICK = ["e02", "e03", "e05", "e06", "e08", "e12"]
# 일레븐랩스 목소리와 비슷한 성별·느낌으로 고른다. (작성자 판단)
VOICE = {"해설자": "Sulafat", "남1": "Puck", "여1": "Aoede", "남2": "Iapetus", "여2": "Leda"}
STYLE = {"[casual]": "casually, like chatting with a friend", "[tired]": "in a tired, worn-out voice",
         "[sighs]": "with a sigh, a little down", "[excited]": "excitedly", "[nervous]": "nervously",
         "[worried]": "in a worried, hurried voice"}


def key():
    for l in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if l.startswith("GEMINI_API_KEY="):
            return l.split("=", 1)[1].strip()
    sys.exit("GEMINI_API_KEY 없음")


def main(model, only=None):
    out = HERE / "audio" / "unused" / "google-test" / (model + "-v2")
    out.mkdir(parents=True, exist_ok=True)
    k = key()
    clips = {c["id"]: c for c in json.loads(CLIPS.read_text(encoding="utf-8"))}
    for cid in (only or PICK):
        c = clips[cid]
        tag, text = c["say"].split(" ", 1)
        mp3 = out / f"{cid}.mp3"
        if mp3.exists():
            continue
        # 지시문을 따로 두지 않으면 지시문까지 읽어 버린다(첫 시험). 연출 메모와 대본을 나눠 적는다.
        notes = (f"Speak {STYLE[tag]}. Natural American English, everyday conversation." if c["who"] != "해설자" else
                 "Speak in natural standard Seoul Korean, as a kind, calm female teacher explaining to a beginner, "
                 "polite and friendly. Say the English words in it with natural American pronunciation.")
        prompt = (f"### DIRECTOR'S NOTES\n{notes}\n"
                  f"Read only the transcript below, nothing else.\n\n#### TRANSCRIPT\n{text}")
        body = {"contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseModalities": ["AUDIO"],
                                     "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE[c["who"]]}}}}}
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                                     data=json.dumps(body).encode(), headers={"x-goog-api-key": k, "Content-Type": "application/json"})
        for attempt in range(4):
            try:
                d = json.load(urllib.request.urlopen(req, timeout=120))
                break
            except urllib.error.HTTPError as e:
                msg = e.read().decode()[:300]
                if e.code == 429 and attempt < 3:
                    print(cid, "429, 30초 기다림")
                    time.sleep(30)
                    continue
                sys.exit(f"{cid} HTTP {e.code}: {msg}")
        part = d["candidates"][0]["content"]["parts"][0]["inlineData"]
        # 3.8 모델은 헤더 있는 WAV(audio/wav)를 준다. 날 PCM으로 읽으면 헤더와 꼬리 정보가 "치지직" 잡음이 된다(2026-11-09).
        mime = part.get("mimeType", "")
        pcm = out / f"{cid}.{'wav' if 'wav' in mime else 'pcm'}"
        pcm.write_bytes(base64.b64decode(part["data"]))
        rate = int(mime.split("rate=")[1].split(";")[0]) if "rate=" in mime else 24000
        fmt = [] if "wav" in mime else ["-f", "s16le", "-ar", str(rate), "-ac", "1"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", *fmt, "-i", str(pcm),
                        "-af", "loudnorm=I=-16:TP=-1.5", "-c:a", "libmp3lame", "-b:a", "128k", str(mp3)], check=True)
        pcm.unlink()
        print(cid, VOICE[c["who"]], text, "완료")
        time.sleep(4)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:] or None)
