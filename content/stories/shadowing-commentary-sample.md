# 쉐도잉 한국어 해설 견본: Small Talk 1화 How's It Going? (2026-11-11, 검토용)

성범 요청: 쉐도잉에 한국어 해설을 어떻게 넣을지 1화로 풀 대본을 만들어 보기.

**견본 음성 (2026-11-11 성범 "1화 만들어 봐"):** 해설자 Mina, eleven_v4, `[casual]`, 한 번씩 만들어 4마디 230크레딧(56+52+72+50). 조각은 `spikes/episode-01/audio/shadowing/small-talk/ep01/commentary/n1~n4.mp3`, 이은 판은 `audio/shadowing/trim-test/sample-ep01.mp3`(1분 39초, 지금 앱 1분 12초). 앱에는 아직 넣지 않았다.

**해설 목소리 JISOO로 바꿈 (2026-11-11 성범 "다른 여성의 목소리로"):** 후보 10개를 미리 듣기로 듣고 JISOO, Kanna, Hana Lee로 같은 문장(n2)을 만들어 비교한 뒤 JISOO를 골랐다(156크레딧). n1, n3, n4를 JISOO로 다시 만들었다(56+72+50=178크레딧). Mina 조각은 `commentary/mina/`, Mina로 이은 판은 `trim-test/sample-ep01-mina.mp3`. 지금 `sample-ep01.mp3`는 JISOO판(1분 38초). 이은 방법은 build_shadowing.py 흐름에 해설을 끼운 시험 코드로, 확정되면 build_shadowing.py에 옮긴다.

## 짜임 (`작성자 판단`)

- 대화 앞에 장면 소개 한 줄, 따라 하기에서는 핵심 줄 앞마다 해설 한두 문장. 마무리 정리는 넣지 않는다.
- 대화(Listen, Listen again)는 영어만 둔다. 안내 "Now, repeat after me.", "One more time."도 영어 그대로 쓴다(이미 만든 소리).
- 해설자는 존댓말 강사 말투이고 이름은 부르지 않는다. 영어 문장을 해설자가 직접 읽지 않고, 바로 뒤에 영어 목소리로 들려준다. 발음 팁만 한글로 적는다.
- 따라 하기 줄은 정리안(`shadowing-repeat-review.md`)대로 앞 감탄사를 뗀 문장이다.

## 대본

```text
[시작음]

해설자: 아침에 회사 1층 카페에서 아는 동료를 만났어요. 가볍게 인사하고 헤어지는 대화예요.

── Listen ──
Me:    Hey! How's it going?
Sarah: Oh, hey! Not bad. You?
Me:    Pretty good. Just grabbing some coffee.
Sarah: Same here. I can't function without it.
Me:    I feel you.
Sarah: Alright, I gotta run. See you around!
Me:    See you!

── Repeat ──
안내:  Now, repeat after me.

해설자: '잘 지내요?'라는 뜻이에요. 아는 사람을 만났을 때 가볍게 건네는 인사예요.
Me:    How's it going?                          (멈춤)
Me:    How's it going?                          (멈춤) [클릭음]

해설자: '꽤 좋아요. 커피 좀 사러 왔어요.'라는 말이에요. 커피 사는 부분은 '그래빙썸 커피'처럼 붙여서 말해 보세요.
Me:    Pretty good. Just grabbing some coffee.  (멈춤)
Me:    Pretty good. Just grabbing some coffee.  (멈춤) [클릭음]

해설자: '무슨 말인지 알아요'라는 뜻이에요. 상대 말에 맞장구칠 때 편하게 써요.
Me:    I feel you.                              (멈춤)
Me:    I feel you.                              (멈춤) [클릭음]

── Listen again ──
안내:  One more time.
(대화 전체를 한 번 더)
```

## 가사 화면

- 해설자 줄은 코스 해설처럼 한국어 줄로 보인다. 따라 하기 영어 줄 아래 한글 뜻은 해설이 이미 말하므로 숨긴다(말해보기 정답과 같다).

## 길이와 비용 어림

- 새로 만들 소리는 해설 4마디, 한국어 약 170자. 약 170~200크레딧.
- 트랙은 약 1분 20초에서 1분 45초 정도로 늘어난다.
- 70화 전체로 하면 약 1만 2천~1만 4천 크레딧. 만들기 전에 정확한 숫자를 다시 말씀드린다.
