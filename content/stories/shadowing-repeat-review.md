# 쉐도잉 따라 하기 줄 정리안 (2026-11-11)

성범 요청: "따라해보세요" 부분에서 필요 없는 감탄사와 덧붙인 말은 빼고 알짜만 남기기.

**적용 (2026-11-11, 성범이 견본 16줄을 듣고 "오 좋다", "오디오 자르기부터"):** 각 앨범 대본(`shadowing-<앨범>.md`)의 핵심 줄 뜻 아래에 `따라: 영어 | 한국어 | 앞 0.62` 또는 `따라: 뺌`을 적었고, `build_shadowing.py`가 이 줄을 읽어 따라 하기에서 자른 소리와 자른 글·뜻을 쓴다. 52줄 자름, 2줄 뺌.
- 자를 자리는 줄 소리의 10ms 음량에서 쉼 구간 가운데를 골랐다. 성범이 들은 16줄은 그 자리 그대로, 나머지는 자동으로 고른 뒤 쉼이 여러 개인 줄은 손으로 골랐다(Small Talk 9화는 "Let me see." 뒤가 아니라 "Oh," 뒤 1.85초).
- **Social Skills 6화 "Oh no, I'm so sorry! Are you okay?"는 자르지 않고 그대로 둔다.** "Oh no"와 "I'm" 사이에 쉼이 전혀 없어 자르면 첫소리가 끊긴다. 바꾸려면 그 줄만 새로 만든다(약 50크레딧).
- Small Talk 5화 "It's just been a crazy week."는 쉼이 얕아(약 -38dB) 들어 보고 어색하면 새로 만든다.

## 정한 기준 (`작성자 판단`, 성범 확인 전)

- **대화(Listen, Listen again)는 그대로 둔다.** 감탄사는 실제 말투라 들려주기에서는 살린다. 바꾸는 건 따라 하기(Repeat) 부분만이다.
- **자르기:** 줄 앞의 Yeah, Oh, Whoa, Hey, Wow, Ha, Well, Okay, Sure, Great처럼 누구나 따라 할 수 있는 말을 뗀다.
- **남기기:** 그 자체가 배울 표현이면 남긴다. 예를 들어 Excuse me, Sorry, Actually, Honestly, Seriously?, Wait, Totally, Deal, Hi, it's me(전화)가 그렇다. 욕설 앨범의 Holy shit, Damn, Shut up 같은 감탄도 배울 내용이라 남긴다.
- **빼기:** 따라 해도 남는 게 없는 줄(철자 읽기, Yes, please)은 따라 하기에서 뺀다. 한 화의 핵심 줄이 2개가 되어도 괜찮다(규칙은 2~3개).
- 여기 없는 줄은 지금 그대로다.

## 만드는 법과 비용

- 따라 하기 소리는 대화에서 만든 줄 소리(d1, d2 …)를 다시 쓴다. 앞을 자를 때는 그 소리에서 쉼표 뒤 쉬는 자리를 찾아 잘라 쓴다. **일레븐랩스 비용은 0원이다.**
- 자르는 방법: ffmpeg로 쉼표 뒤 쉬는 구간(소리가 거의 없는 곳) 가운데를 자르고, 자른 첫머리에 짧은 페이드인(약 15ms)을 넣어 '틱' 소리를 막는다. 가운데만 덜어내고 앞뒤를 잇는 자르기는 하지 않는다. 억양이 이어지지 않아 티가 나기 쉽다.
- 먼저 몇 줄만 잘라 성범이 들어 보고 괜찮으면 전체에 쓴다.
- 가사에는 자른 문장이 그대로 보인다(대본에 따라 하기용 글을 따로 적는다).
- 쉼 없이 붙어 나오는 줄(아래 '방법'에 **붙음**이라고 표시)은 자르면 첫소리가 끊길 수 있다. 들어 보고 어색하면 그 줄만 새로 만든다(한 줄에 약 50크레딧). 새로 만들 때는 미리 말씀드린다.
- 쉐도잉에 한국어 해설을 넣을지는 따로 정한다. 이 정리와는 상관없다.

## 1. Small Talk (9줄 자름)

| 화 | 지금 | 바꿀 안 | 방법 |
|---|---|---|---|
| 1 | Hey! How's it going? | How's it going? | 앞 자르기 |
| 2 | Whoa, long time no see! | Long time no see! | 앞 자르기 |
| 2 | Yeah, same old, same old. What about you? | Same old, same old. What about you? | 앞 자르기 |
| 5 | Yeah, it's just been a crazy week. | It's just been a crazy week. | 앞 자르기 |
| 6 | Oh yeah? Any recommendations? | Any recommendations? | 앞 자르기 |
| 7 | Yeah, it helps me clear my head. | It helps me clear my head. | 앞 자르기 |
| 8 | Wow, this line is so long. | This line is so long. | 앞 자르기 |
| 9 | Let me see. Oh, it's not far from here. | It's not far from here. | 앞 자르기(가운데만 덜어내면 이음새가 어색해서 쓰지 않는다) |
| 10 | Oh, look at the time. I should get going. | Look at the time. I should get going. | 앞 자르기 |

## 2. Daily Routine (8줄 자름)

| 화 | 지금 | 바꿀 안 | 방법 |
|---|---|---|---|
| 1 | Yeah, I'm kind of a morning person. | I'm kind of a morning person. | 앞 자르기 |
| 1 | Ha, it just takes some getting used to. | It just takes some getting used to. | 앞 자르기 |
| 2 | Yeah, I work out before work. | I work out before work. | 앞 자르기 |
| 2 | Legs. I'm going to be sore tomorrow. | I'm going to be sore tomorrow. | 앞 자르기 |
| 4 | Okay. Let me grab a coffee first. | Let me grab a coffee first. | 앞 자르기 |
| 6 | Yeah, it's due today. | It's due today. | 앞 자르기 |
| 8 | Yeah, let's order something. | Let's order something. | 앞 자르기 |
| 9 | Laundry, cleaning... my place is a mess. | My place is a mess. | 앞 자르기 |

## 3. About Me (9줄 자름, 1줄 뺌)

| 화 | 지금 | 바꿀 안 | 방법 |
|---|---|---|---|
| 1 | Oh, so you're the coworker she always talks about. | So you're the coworker she always talks about. | 앞 자르기 |
| 2 | S-E-O-N-G, B-E-O-M. | (뺌) | 철자 읽기는 따라 할 게 없다 |
| 2 | Yeah. You can just call me Beom if that's easier. | You can just call me Beom if that's easier. | 앞 자르기 |
| 3 | Yeah, born and raised. | Born and raised. | 앞 자르기 |
| 4 | It is. It keeps me busy, though. | It keeps me busy, though. | 앞 자르기 |
| 7 | Yeah, I saw a few when they came to Seoul. | I saw a few when they came to Seoul. | 앞 자르기 |
| 7 | It was! Here, let me play you one of my favorites. | Let me play you one of my favorites. | 앞 자르기 |
| 9 | Yeah, I'm going to see my parents. | I'm going to see my parents. | 앞 자르기 |
| 9 | Yeah, and he's the cutest. | He's the cutest. | 앞 자르기, **붙음** |
| 10 | Sure. Hi, everyone. I'm Seongbeom, and I'm from Seoul. | Hi, everyone. I'm Seongbeom, and I'm from Seoul. | 앞 자르기 |

남기는 것: 2화 "It's Seongbeom."(이름 말하는 틀), 5화 "Totally. My boss is pretty chill, too."(Totally가 배울 말).

## 4. Eating Out (8줄 자름, 1줄 뺌)

| 화 | 지금 | 바꿀 안 | 방법 |
|---|---|---|---|
| 1 | Hi, can I get a grande iced Americano? | Can I get a grande iced Americano? | 앞 자르기 |
| 1 | It's Beom. B-E-O-M. | It's Beom. | 뒤 철자 자르기 |
| 2 | Hi, can I get a tall vanilla latte? | Can I get a tall vanilla latte? | 앞 자르기 |
| 5 | Great. I'll wait over there. | I'll wait over there. | 앞 자르기 |
| 6 | Hi, can I get a footlong chicken teriyaki on wheat? | Can I get a footlong chicken teriyaki on wheat? | 앞 자르기 |
| 6 | Yes, please. | (뺌) | 너무 쉽다 |
| 7 | Hi, a table for two, please. | A table for two, please. | 앞 자르기 |
| 7 | No, we don't. Is there a wait? | Is there a wait? | 앞 자르기 |
| 9 | Yes, everything was great. | Everything was great. | 앞 자르기 |

남기는 것: "A Coke Zero, please.", "To go, please.", "Hot, please."(주문할 때 바로 쓰는 틀), "Deal. Let's go get some."

## 5. Social Skills (9줄 자름)

| 화 | 지금 | 바꿀 안 | 방법 |
|---|---|---|---|
| 1 | Whoa, nice shoes! Are they new? | Nice shoes! Are they new? | 앞 자르기 |
| 2 | Hey, you nailed that presentation. | You nailed that presentation. | 앞 자르기 |
| 4 | Oh, I wish I could help, but I already have plans. | I wish I could help, but I already have plans. | 앞 자르기 |
| 4 | Sure. I'll bring some food, too. | I'll bring some food, too. | 앞 자르기 |
| 6 | Oh no, I'm so sorry! Are you okay? | I'm so sorry! Are you okay? | 앞 자르기 |
| 6 | Here, let me get you some napkins. | Let me get you some napkins. | 앞 자르기, **붙음** |
| 8 | Well, I guess we'll have to agree to disagree. | I guess we'll have to agree to disagree. | 앞 자르기 |
| 10 | You too. I had a really good time. | I had a really good time. | 앞 자르기 |
| 10 | Great. I'll text you so you have mine. | I'll text you so you have mine. | 앞 자르기 |

## 6. Speak Up (5줄 자름)

| 화 | 지금 | 바꿀 안 | 방법 |
|---|---|---|---|
| 2 | Hey, sorry to bother you, but can you keep it down? | Sorry to bother you, but can you keep it down? | 앞 자르기 |
| 5 | Whoa. Don't talk to me like that. | Don't talk to me like that. | 앞 자르기 |
| 8 | Hey, hold on. Let's not fight about this. | Hold on. Let's not fight about this. | 앞 자르기 |
| 10 | Sounds good. So, are we good? | Are we good? | 앞 자르기 |
| 10 | Great. Let me buy you a drink. | Let me buy you a drink. | 앞 자르기 |

남기는 것: "Excuse me, I was here first.", "Wait, that's not what I said.", "Seriously? You always do this.", "Honestly, I was hurt…"(앞말이 곧 표현).

## 7. Swearing (5줄 자름)

욕과 감탄이 배울 내용이라 대부분 그대로 둔다. 욕이 없는 앞말만 뗀다.

| 화 | 지금 | 바꿀 안 | 방법 |
|---|---|---|---|
| 2 | No, nothing. How the hell am I supposed to get out? | How the hell am I supposed to get out? | 앞 자르기 |
| 2 | Good idea. I'm gonna be late as hell. | I'm gonna be late as hell. | 앞 자르기 |
| 5 | Yeah. And they're not even paying extra. | And they're not even paying extra. | 앞 자르기 |
| 8 | Yeah. I'm so fucking tired. | I'm so fucking tired. | 앞 자르기 |
| 9 | Right? It pissed me off so much. | It pissed me off so much. | 앞 자르기 |

남기는 것: "Yeah, yeah. Fuck off."(Yeah, yeah가 '알았어 알았어' 하는 말투라 표현의 일부).

## 합계

210줄 가운데 53줄을 자르고 2줄을 뺀다. 나머지 155줄은 그대로다.
