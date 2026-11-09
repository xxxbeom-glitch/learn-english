"""심화, 고급 음성 시험판(2026-11-10). beginner_v2.py와 같은 짜임으로 만들고, 다른 점만 여기에 둔다.

다른 점:
- 대본: content/stories/course-intermediate.md, course-advanced.md
- '### 끝인사'는 초급처럼 말해보기 끝에 이어 붙이고, '### 검수 메모'는 읽지 않는다.
- 시작음: 심화 sfx-start-intermediate.mp3, 고급 sfx-start-advanced.mp3 (2026-11-10 성범이 일레븐랩스 효과음에서 고름).
  고급 소리는 평균 음량이 약 5dB 커서 더 줄여 초급 시작음과 맞춘다. 끝음과 말해보기 클릭음은 초급 것을 쓴다.
- 결과: audio/<과정>/epNN/<i|a>-NN.mp3 (앱 폴더에는 아직 넣지 않는다).

python course_v2.py clips intermediate 1   조각 목록(clips.json)
python course_v2.py build intermediate 1   조각 이어 붙이기
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import beginner_v2 as b
from build_page import parse

HERE = Path(__file__).parent
STORIES = HERE.parent.parent / "content" / "stories"
COURSE = {
    "intermediate": {"file": "course-intermediate.md", "tag": "i", "start": ("sfx-start-intermediate.mp3", "-9dB")},
    "advanced": {"file": "course-advanced.md", "tag": "a", "start": ("sfx-start-advanced.mp3", "-13dB")},
}


def episode(course, n):
    text = (STORIES / COURSE[course]["file"]).read_text(encoding="utf-8")
    text = re.sub(r"^### 검수 메모\n.*?(?=^## |\Z)", "", text, flags=re.M | re.S)
    text = re.sub(r"^### 끝인사\n", "", text, flags=re.M)
    return next(e for e in parse(text) if e["n"] == n)


def setup(course, n):
    """beginner_v2의 함수를 이 과정에 맞게 돌린다."""
    out = HERE / "audio" / course
    b.OUT = b.SOUNDS = out
    b.episode = lambda _n: episode(course, n)
    return out / f"ep{n:02d}"


def clips(course, n):
    setup(course, n)
    b.clips(n)


def build(course, n):
    d = setup(course, n)
    c = COURSE[course]
    start, vol = c["start"]
    # beginner_v2.build의 시작음, 파일 이름, 앱 폴더를 이 과정 것으로 바꿔서 부른다.
    real_run = subprocess.run
    name = f"{c['tag']}-{n:02d}"

    def run(cmd, *a, **k):
        cmd = [str(x) for x in cmd]
        cmd = [x.replace("sfx-start.mp3", start) for x in cmd]
        if any(start in x for x in cmd):
            cmd = [x.replace("volume=-9dB", f"volume={vol}") for x in cmd]
        cmd = [x.replace(f"b1-{n:02d}-v2.mp3", f"{name}.mp3") for x in cmd]
        cmd = [x.replace(str(b.APP / f"b1-{n:02d}-v2.webm"), str(d / f"{name}.webm")) for x in cmd]
        return real_run(cmd, *a, **k)

    b.subprocess.run = run
    real_dur = b.dur
    b.dur = lambda p: real_dur(d / f"{name}.webm") if str(p) == str(b.APP / f"b1-{n:02d}-v2.webm") else real_dur(p)
    try:
        b.build(n)
    finally:
        b.subprocess.run, b.dur = real_run, real_dur
    tl = json.loads((d / "timeline.json").read_text(encoding="utf-8"))
    tl["file"] = f"{name}.webm"
    (d / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    {"clips": clips, "build": build}[sys.argv[1]](sys.argv[2], int(sys.argv[3]))
