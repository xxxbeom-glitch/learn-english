"""해설자 목소리 고르기 (2026-11-09). 1화 도입 해설 한 덩어리를 구글 Gemini 목소리 몇 개로 읽혀 짧은 트랙 하나로 잇는다. 시험판 코드다.

python voice_audition.py  → audio/google-test/narrator-audition/<목소리>.mp3, app/b1-01-voices.webm, 시간표 json
성범 요청: 20대 중후반 여성 목소리. 지금 Sulafat은 너무 어려 보이고, 줄마다 억양이 달라 두 사람 같다.
"""
import base64
import json
import subprocess
import time
import urllib.request
from pathlib import Path

from google_tts_test import key

HERE = Path(__file__).parent
OUT = HERE / "audio" / "google-test" / "narrator-audition"
APP = HERE / "app"
MODEL = "gemini-3.8-flash-tts"
CLIP = json.loads((HERE / "audio" / "beginner2" / "ep01" / "clips.json").read_text(encoding="utf-8"))[0]
TEXT = CLIP["say"].split(" ", 1)[1]  # n01 도입 해설
# 차분하고 어른스러운 쪽으로 알려진 여성 목소리. (작성자 판단)
VOICES = ["Despina", "Erinome", "Vindemiatrix"]  # 성범: 같은 문장을 세 명 정도로
# 나이와 말투를 고정해 적어 두면 줄마다 억양이 흔들리는 것을 줄일 수 있다. 모든 줄에 같은 글을 쓴다.
PROFILE = ("# AUDIO PROFILE\nA Korean woman in her mid-to-late twenties (about 27). Calm, warm, mature voice with a "
           "medium-low pitch. Not childlike, not cute, not bubbly.\n\n### DIRECTOR'S NOTES\nShe is an English teacher "
           "explaining to a beginner in polite Korean (해요체). Natural standard Seoul Korean. Steady, unhurried pace and "
           "even, consistent intonation from start to end, with no exaggerated ups and downs. Say the English words in it "
           "with natural American pronunciation. Read only the transcript below, nothing else.\n\n#### TRANSCRIPT\n")
# 2차(성범: 위 셋은 중성적이다. "예쁜 여자가 설명해 주는" 느낌으로 3개 더). 여성스럽고 고운 쪽으로 알려진 목소리. (작성자 판단)
VOICES2 = ["Achernar", "Autonoe", "Aoede"]
PROFILE2 = ("# AUDIO PROFILE\nA Korean woman in her mid-to-late twenties (about 27). A clearly feminine, pretty, sweet and "
            "warm voice, soft and lovely, like a kind young female announcer. Grown-up, not childish or cute-acting.\n\n"
            "### DIRECTOR'S NOTES\nShe is an English teacher kindly explaining to a beginner in polite Korean (해요체), "
            "with a gentle smile in her voice. Natural standard Seoul Korean. Steady, unhurried pace and even, consistent "
            "intonation from start to end. Say the English words in it with natural American pronunciation. "
            "Read only the transcript below, nothing else.\n\n#### TRANSCRIPT\n")
VOICES += VOICES2


def gen(voice):
    mp3 = OUT / f"{voice}.mp3"
    if mp3.exists():
        return mp3
    body = {"contents": [{"parts": [{"text": (PROFILE2 if voice in VOICES2 else PROFILE) + TEXT}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
                                 data=json.dumps(body).encode(), headers={"x-goog-api-key": key(), "Content-Type": "application/json"})
    part = json.load(urllib.request.urlopen(req, timeout=120))["candidates"][0]["content"]["parts"][0]["inlineData"]
    assert "wav" in part["mimeType"], part["mimeType"]  # WAV로 읽어야 끝에 잡음이 생기지 않는다
    wav = OUT / f"{voice}.wav"
    wav.write_bytes(base64.b64decode(part["data"]))
    cut = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-af", cut + ",loudnorm=I=-16:TP=-1.5", "-ar", "44100",
                    "-ac", "1", "-c:a", "libmp3lame", "-b:a", "128k", str(mp3)], check=True)
    wav.unlink()
    print(voice, "완료")
    time.sleep(4)
    return mp3


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                check=True, capture_output=True, text=True).stdout)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "tmp"
    tmp.mkdir(exist_ok=True)
    parts, lines, t = [], [], 0.0

    def silence(sec):
        nonlocal t
        p = tmp / f"s{len(parts)}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(sec),
                        "-c:a", "pcm_s16le", str(p)], check=True)
        parts.append(p); t += sec

    def sound(src, af):
        nonlocal t
        p = tmp / f"c{len(parts)}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", af, "-ar", "44100", "-ac", "1",
                        "-c:a", "pcm_s16le", str(p)], check=True)
        parts.append(p); d = dur(p); t += d
        return d

    silence(0.5)
    for k, v in enumerate(VOICES, 1):
        a = t
        sound(HERE / "audio" / "raw" / "sfx-next-soft.mp3", "atrim=0:1.0,afade=t=out:st=0.9:d=0.1,volume=-4dB")
        silence(0.5)
        lines.append({"section": "intro", "speaker": "목소리", "text": f"목소리 {k} · {v}", "meaning": None, "kind": "line",
                      "start": round(a, 2), "end": round(t, 2)})
        a = t
        d = sound(gen(v), "anull")
        sents = [s for s in TEXT.replace("? ", "?|").replace(". ", ".|").split("|")]
        total, x = sum(len(s) for s in sents), a
        for i, s in enumerate(sents):
            y = a + d if i == len(sents) - 1 else x + d * len(s) / total
            lines.append({"section": "intro", "speaker": "해설자", "text": s, "meaning": None, "kind": "line",
                          "start": round(x, 2), "end": round(y, 2)})
            x = y
        silence(1.0)
    listing = tmp / "list.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    mp3 = OUT / "b1-01-voices.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c:a", "libmp3lame",
                    "-b:a", "128k", str(mp3)], check=True)
    name = "b1-01-voices.webm"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-ac", "1", "-c:a", "libopus", "-b:a", "24k", str(APP / name)], check=True)
    tl = {"duration": round(dur(APP / name), 2), "sections": [{"key": "intro", "title": "도입", "start": 0}], "lines": lines, "file": name}
    (OUT / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{tl['duration']:.1f}초", len(lines), "줄")


def timeline():
    p = OUT / "timeline.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() and (APP / "b1-01-voices.webm").exists() else None


if __name__ == "__main__":
    main()
