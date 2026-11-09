"""1화 시험판 조립 스크립트. 버리는 코드다.

인물별 일레븐랩스 생성본을 대본 줄 단위로 잘라
한 화 순서로 다시 붙이고, 앱 화면이 쓸 시간표 JSON을 만든다.
"""
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
RAW = HERE / "audio" / "raw"
TMP = HERE / "audio" / "tmp"
OUT = HERE / "audio" / "episode-01.mp3"
TIMELINE = HERE / "audio" / "timeline.json"

SPEAK_PAUSE = 3.0  # 말해보기에서 직접 말할 시간
SR = 44100
TAYLOR4_END = 1.039388  # taylor-4.mp3 말끝

# 인물별 원본 파일에서 줄 구간을 잘라 쓴다. (시작, 끝)은 silencedetect로 찾은 값이다.
T = {
    "t1": ("Taylor", "taylor", 0.00, 2.88), "t2": ("Taylor", "taylor-2", 0.00, 2.44),
    "t3": ("Taylor", "taylor-2", 3.47, 7.28), "t4": ("Taylor", "taylor", 10.72, 12.54),
    "t5": ("Taylor", "taylor-2", 8.52, 10.58), "t6": ("Taylor", "taylor", 15.97, 19.24),
    "t7": ("Taylor", "taylor-3", 0.00, 6.60), "t8": ("Taylor", "taylor", 23.04, 23.83),
    "t9": ("Taylor", "taylor-4", 0.00, TAYLOR4_END), "t10": ("Taylor", "taylor", 26.93, 27.54),
    "t11": ("Taylor", "taylor-2", 18.37, 19.06),
    "j1": ("Justin", "justin-2", 0.00, 2.05), "j2": ("Justin", "justin", 3.70, 5.76),
    "j3": ("Justin", "justin", 6.77, 8.76), "j4": ("Justin", "justin-2", 3.29, 10.13),
    "j5": ("Justin", "justin", 14.51, 17.31), "j6": ("Justin", "justin-3", 0.00, 4.01),
    "j7": ("Justin", "justin-2", 14.66, 15.20), "j8": ("Justin", "justin", 23.79, 24.51),
    "j9": ("Justin", "justin", 25.25, 25.89), "j10": ("Justin", "justin", 26.59, 27.44),
    "j11": ("Justin", "justin", 28.04, 28.59), "j12": ("Justin", "justin", 29.26, 29.83),
}

DIALOGUE = [
    ("t1", "Oh no... why isn't this working?", "아이고... 이게 왜 안 되지?"),
    ("j1", "Uh... excuse me?", "저... 저기요?"),
    ("t2", "Oh, hi! Do you speak English?", "아, 안녕하세요! 영어 하세요?"),
    ("j2", "A little. Where are you going?", "조금요. 어디 가세요?"),
    ("t3", "Um... Hong... Hongdae? Is that right?", "음... 홍... 홍대? 이거 맞아요?"),
    ("j3", "Ah, Hongdae. Let me help you.", "아, 홍대요. 제가 도와드릴게요."),
    ("t4", "Oh, thank you so much!", "아, 정말 고마워요!"),
    ("j4", "Put your card here. Okay. Line 3, and then... um... change? Change train?", "여기에 카드 올리세요. 됐어요. 3호선 타고, 그다음에... 음... 바꿔요? 기차 바꿔요?"),
    ("t5", "Oh, transfer?", "아, 갈아타라고요?"),
    ("j5", "Yes! Transfer. Line 2. You're all set.", "네! 갈아타요. 2호선이요. 다 됐어요."),
    ("t6", "You saved me. I'm Taylor. I just moved to Seoul.", "덕분에 살았어요. 저는 테일러예요. 얼마 전에 서울로 왔어요."),
    ("j6", "I'm Seongbeom. Um... go carefully?", "저는 성범이에요. 음... 조심해서 가요?"),
    ("t7", "Go carefully? You mean take care? You too. Bye, Seong... Seongbeom!", "조심해서 가라고요? 조심히 가세요, 말이죠? 성범 씨도요. 안녕히 가세요!"),
    ("j7", "...Bye.", "...안녕히 가세요."),
]


def s(src, start, end, text):
    return ("해설자", src, start, end, text, None)


def e(key, text, meaning):
    who, src, start, end = T[key]
    return (who, src, start, end, text, meaning)


N = "narrator-mina"  # 해설자 음성 Mina. 구간은 silencedetect와 단어 시간으로 찾았다.

COMMENTARY = [
    s(N, 0.00, 2.69, "야 성범아, 아까 진짜 잘했어."),
    s(N, 3.08, 5.80, "모르는 외국인한테 네가 먼저 말 걸었잖아."),
    s(N, 6.14, 8.19, "그게 제일 어려운 건데 해냈어."),
    s(N, 8.80, 11.16, "오늘은 네가 쓴 표현 세 개만 챙겨 가자."),
    s(N, 11.75, 14.10, "첫 번째, 네가 이렇게 물었지."),
    e("j8", "Where are you going?", "어디 가세요?"),
    s(N, 14.60, 16.37, "어디 가세요, 이런 뜻이야."),
    s(N, 16.97, 20.06, "길 헤매는 사람한테 제일 먼저 꺼내기 좋은 말이야."),
    s(N, 20.68, 23.53, "앞은 그대로 두고 뒤만 바꾸면 이렇게도 써."),
    e("t8", "Where are you from?", "어디서 오셨어요?"),
    s(N, 24.17, 25.15, "어디서 오셨어요?"),
    s(N, 25.74, 28.04, "처음 만난 사람한테 자주 하는 질문이야."),
    s(N, 28.83, 31.62, "두 번째는 제가 도와드릴게요, 라는 말."),
    e("j9", "Let me help you.", "제가 도와드릴게요."),
    s(N, 32.14, 33.45, "앞부분만 다시 들어 봐."),
    e("j10", "Let me", "제가 ~할게요"),
    s(N, 34.10, 38.26, "이 말 뒤에 내가 할 일을 붙이면, 제가 할게요, 라는 말이 돼."),
    s(N, 38.82, 39.92, "그래서 이렇게도 써."),
    e("j11", "Let me check.", "제가 확인해 볼게요."),
    s(N, 40.46, 41.55, "제가 확인해 볼게요."),
    s(N, 42.28, 43.31, "하나만 조심하자."),
    s(N, 43.69, 45.28, "이렇게 말하면 뜻이 달라져."),
    e("t9", "Can you help me?", "나 좀 도와주세요."),
    s(N, 45.83, 47.81, "나 좀 도와주세요, 라는 말이 돼."),
    s(N, 48.72, 51.88, "세 번째는 네가 교통카드 충전해 주고 한 말이야."),
    e("j12", "You're all set.", "다 됐어요."),
    s(N, 52.46, 55.56, "다 됐어요, 이제 준비 끝났어요, 라는 뜻이야."),
    s(N, 56.19, 59.42, "가게에서 계산 끝났을 때 직원도 자주 쓰는 말이야."),
    s(N, 60.16, 64.16, "그리고 네가 막혔던 말, 갈아타기는 영어로 이렇게 말해."),
    e("t10", "Transfer.", "갈아타기"),
    s(N, 64.85, 69.39, "단어가 생각 안 나서 쉬운 말로 돌려 말했는데, 그래도 뜻은 통했잖아."),
    s(N, 69.65, 70.55, "그거면 충분해."),
    s(N, 71.43, 76.34, "헤어질 때 하고 싶었던 말, 조심히 가세요는 이렇게 말하면 자연스러워."),
    e("t11", "Take care.", "조심히 가세요."),
    s(N, 77.09, 79.07, "자, 이제 네가 직접 말해 보자."),
    s(N, 79.64, 81.91, "한국어 듣고, 영어를 먼저 떠올려 봐."),
]

# 말해보기: (한국어 시작, 끝, 영어 줄 키, 한국어, 영어)
PRACTICE = [
    (82.76, 83.47, "j8", "어디 가세요?", "Where are you going?"),
    (84.15, 85.30, "j9", "제가 도와드릴게요.", "Let me help you."),
    (85.90, 86.68, "j12", "다 됐어요.", "You're all set."),
]

BRIDGE = [
    s(N, 87.26, 90.41, "잘했어. 이제 아까 대화 다시 들어 보자."),
    s(N, 90.85, 92.48, "아까보다 잘 들릴 거야."),
]

LINE_GAP = 0.35  # 줄 사이 숨
PAD = 0.06  # 말끝이 잘리지 않게 앞뒤로 조금 더 자른다
SOURCES = ["taylor", "taylor-2", "taylor-3", "taylor-4", "justin", "justin-2", "justin-3", N]


def run(*args):
    subprocess.run(args, check=True, capture_output=True)


def loudness(name):
    """파일마다 음량이 달라서 원본별로 맞춘다."""
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(RAW / f"{name}.mp3"), "-af", "ebur128=framelog=quiet",
                          "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", out)[-1])


class Builder:
    def __init__(self):
        self.parts = []
        self.t = 0.0
        self.lines = []
        self.sections = []
        self.gain = {n: -18 - loudness(n) for n in SOURCES}
        TMP.mkdir(parents=True, exist_ok=True)

    def _add_file(self, path):
        self.parts.append(path)
        dur = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)],
            check=True, capture_output=True, text=True).stdout)
        self.t += dur
        return dur

    def silence(self, seconds):
        p = TMP / f"s{len(self.parts):03d}.wav"
        run("ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono",
            "-t", f"{seconds}", "-c:a", "pcm_s16le", str(p))
        self._add_file(p)

    def clip(self, src, start, end):
        p = TMP / f"c{len(self.parts):03d}.wav"
        run("ffmpeg", "-y", "-i", str(RAW / f"{src}.mp3"), "-ss", f"{max(0, start - PAD)}", "-to", f"{end + PAD}",
            "-af", f"volume={self.gain[src]:.2f}dB,afade=t=in:d=0.01,areverse,afade=t=in:d=0.02,areverse",
            "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(p))
        self._add_file(p)

    def sfx(self, name):
        p = TMP / f"x{len(self.parts):03d}.wav"
        run("ffmpeg", "-y", "-i", str(RAW / name), "-af", "volume=-9dB",
            "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(p))
        self._add_file(p)

    def line(self, section, speaker, src, start, end, text, meaning, kind="line"):
        begin = self.t
        self.clip(src, start, end)
        self.lines.append({
            "section": section, "speaker": speaker, "text": text, "meaning": meaning,
            "kind": kind, "start": round(begin, 2), "end": round(self.t, 2),
        })

    def lines_of(self, section, rows):
        for n, row in enumerate(rows):
            if n:
                self.silence(LINE_GAP)
            self.line(section, *row)

    def section(self, key, title):
        self.sections.append({"key": key, "title": title, "start": round(self.t, 2)})


def main():
    b = Builder()
    b.sfx("sfx-start.mp3")
    b.silence(0.3)

    dialogue = [e(key, text, meaning) for key, text, meaning in DIALOGUE]

    b.section("dialogue", "대화")
    b.lines_of("dialogue", dialogue)
    b.silence(0.8)

    b.section("commentary", "해설")
    b.lines_of("commentary", COMMENTARY)
    b.silence(0.7)

    b.section("practice", "말해보기")
    for ko_start, ko_end, key, ko_text, en_text in PRACTICE:
        b.line("practice", "해설자", N, ko_start, ko_end, ko_text, None, kind="prompt")
        pause_start = b.t
        b.silence(SPEAK_PAUSE)
        b.lines.append({"section": "practice", "speaker": "나", "text": "직접 말해보세요",
                        "meaning": None, "kind": "pause",
                        "start": round(pause_start, 2), "end": round(b.t, 2)})
        who, src, start, end = T[key]
        b.line("practice", who, src, start, end, en_text, ko_text, kind="answer")
        b.silence(0.5)
    b.lines_of("practice", BRIDGE)
    b.silence(0.7)

    b.section("replay", "대화 다시 듣기")
    b.lines_of("replay", dialogue)
    b.silence(0.5)
    b.sfx("sfx-end.mp3")

    listing = TMP / "list.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in b.parts), encoding="utf-8")
    run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "1",
        "-c:a", "libmp3lame", "-b:a", "128k", str(OUT))

    TIMELINE.write_text(json.dumps(
        {"duration": round(b.t, 2), "sections": b.sections, "lines": b.lines},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"길이 {b.t:.1f}초, 줄 {len(b.lines)}개")
    for s in b.sections:
        print(s)


if __name__ == "__main__":
    main()
