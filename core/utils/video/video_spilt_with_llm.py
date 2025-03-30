import os
from dashscope import Generation

content = '''
1
00:00:06,000 --> 00:00:09,500
Participant 1: Hm, what is going on? This is so weird!

2
00:00:10,000 --> 00:00:14,000
Participant 2: It was so fun!

3
00:00:25,500 --> 00:00:29,470
Julian: Art, the expression or application

4
00:00:29,470 --> 00:00:34,550
of human creative skill and imagination. That is how it is defined in the dictionary of

5
00:00:34,550 --> 00:00:38,360
my Macbook. You probably heard the term art therapy thrown around before but today we're

6
00:00:38,360 --> 00:00:43,790
honing on a new type of art therapy designed exclusively to focus in on positive emotions,

7
00:00:43,790 --> 00:00:48,290
personal control, and a sense of meaning. Now you can get the down low on it here, but

8
00:00:48,290 --> 00:00:53,730
full disclosure, watching us test it out ourselves is gonna be more entertaining. Plus, I have

9
00:00:53,730 --> 00:00:56,720
my own art therapist! Pamela: Hey how are you doing?

10
00:00:56,720 --> 00:01:00,940
Julian: I'm good, I'm good, how are you? Pamela: I'm good

11
00:01:00,940 --> 00:01:06,030
Julian: Great! Welcome. Pamela is a registered and board certified art therapist with the

12
00:01:06,030 --> 00:01:10,830
American Art Therapy Association. So, can flexing your artistic muscles really make

13
00:01:10,830 --> 00:01:15,860
you happier? Let's find out! Once again we brought in a selection of subjects.

14
00:01:15,860 --> 00:01:18,810
Now first we gave them a test to measure their current level of happiness.

15
00:01:18,810 --> 00:01:22,990
Participant 3: I nailed it! Julian: You're not done yet, no there's more.

16
00:01:22,990 --> 00:01:26,630
Next we asked them to write a list of things in their life that made them feel happier

17
00:01:26,630 --> 00:01:32,290
or supported. Then we had them assign a color to themselves

18
00:01:32,290 --> 00:01:35,360
and each of the things on their list. P3: I'm just gonna write ladies.

19
00:01:35,360 --> 00:01:38,920
Pamela: [laughs] That works. Julian: I don't think there's any misinterpreting

20
00:01:38,920 --> 00:01:42,400
that. It felt like the right time to rope them into

21
00:01:42,400 --> 00:01:49,400
doing something creative, so we traced a life-sized outline of their body, and told them to fill

22
00:01:49,460 --> 00:01:53,930
it in with the different colors depending on where it resonated for them. We told them

23
00:01:53,930 --> 00:01:58,299
to put a circle in the center that represented themselves. Now they hadn't realized it, but

24
00:01:58,299 --> 00:02:01,830
we put them in a reflective state of mind and in order to complete the exercise, they

25
00:02:01,830 --> 00:02:05,549
had to really focus on how each person or thing contributed to their life.

26
00:02:05,549 --> 00:02:10,599
Pamela: So, what was that like for you? Participant 4: Oh I loved it! I love art and

27
00:02:10,599 --> 00:02:16,319
I love to paint, I used to paint when I was a little girl with my grandma.

28
00:02:16,319 --> 00:02:20,000
Pamela: Oh you did? P4: I just think about my grandma

29
00:02:20,000 --> 00:02:24,670
a lot. She taught me how to paint. Pamela: I noticed the first thing you put

30
00:02:24,670 --> 00:02:27,859
in there was the purple to represent, is that mom?

31
00:02:27,859 --> 00:02:32,549
Participant 5: My mom, yeah, she's like on the shoulder kinda area I guess? My mom actually,

32
00:02:32,549 --> 00:02:36,139
I remember when she used to rub my shoulders whenever I would be sick as a kid.

33
00:02:36,139 --> 00:02:39,029
Pamela: Out of all of these things, what are you most passionate about?

34
00:02:39,029 --> 00:02:46,029
Participant 6: Um, well of course my family. I have seven children and they're spread all

35
00:02:46,659 --> 00:02:51,879
over. There are three in California and I rarely get to see them, so I have to say that

36
00:02:51,879 --> 00:02:54,650
my family is my passion. Pamela: Orange, what is orange?

37
00:02:54,650 --> 00:02:57,560
P3: Orange is ladies. Pamela: The ladies.

38
00:02:57,560 --> 00:03:03,650
P3: Yeah, I've always had an interesting relationship with women over the course of my life. When

39
00:03:03,650 --> 00:03:09,400
I was young, I was always the class clown and it was always difficult for me to connect

40
00:03:09,400 --> 00:03:15,029
with women because they wanted a serious man in their life but I was always trying to make

41
00:03:15,029 --> 00:03:19,359
them laugh. So they were always unattainable presence in my life. Like I was never able

42
00:03:19,359 --> 00:03:24,469
to have a girlfriend when I was a kid so, I feel like that has always been a hurdle

43
00:03:24,469 --> 00:03:27,139
that needs to be dealt with. Pamela: Right.

44
00:03:27,139 --> 00:03:31,879
P3: So when you look at me you just see wow that man is very emotional and very passionate

45
00:03:31,879 --> 00:03:38,879
about a plethora of different things. P2: I see a paint representation of my personality.

46
00:03:40,519 --> 00:03:43,329
Pamela: The first thing you put on here was your dad.

47
00:03:43,329 --> 00:03:48,650
P3: My dad has always been the one that's been there my whole life. I'm a daddy's girl

48
00:03:48,650 --> 00:03:51,019
for sure. Pamela: How is he there for you?

49
00:03:51,019 --> 00:03:56,180
P3: My gosh, I have to be careful what I say around him. Like, when I say "I broke my pencil

50
00:03:56,180 --> 00:04:01,370
today" I'll have 24 packs of pencils on my doorstep the next day. Every time I'm on the

51
00:04:01,370 --> 00:04:05,279
phone with my dad present day, he's like, "well just in case I'm not around tomorrow"

52
00:04:05,279 --> 00:04:09,549
you know, stuff like that. Pamela: Is that hard sometimes for you, when

53
00:04:09,549 --> 00:04:15,599
he makes a joke out of something so big. P3: Yes, but it's just like that.

54
00:04:15,599 --> 00:04:24,800
P1: The one right in the middle, um, is my mom. What is going on? This is so weird! [laughs]

55
00:04:26,000 --> 00:04:33,000
Yeah, cause I think just looking at this, you know she really is like my core. She's

56
00:04:35,419 --> 00:04:42,180
like the foundation upon which everything else is kind of been built upon, so she's

57
00:04:42,180 --> 00:04:47,569
been the example through that kind of guides me to even be able to assess where everything

58
00:04:47,569 --> 00:04:53,080
lies so my mom, yeah. Julian: So, what did we find out. Well, we

59
00:04:53,080 --> 00:04:59,879
saw an average increase in happiness 8.1% with the highest just being 36.7%. What does

60
00:04:59,879 --> 00:05:05,159
this mean? Well, Picasso once said, "Art washes away from the soul the dust of everyday life"

61
00:05:05,159 --> 00:05:09,560
and I am starting to think that dude was on to something. When you engage yourself artistically

62
00:05:09,560 --> 00:05:14,129
and use your imagination, you can help regulate your blood pressure and your heart rate. Now

63
00:05:14,129 --> 00:05:18,389
I know what you're thinking. I'm not an artist. Well don't worry, you don't need to know a

64
00:05:18,389 --> 00:05:24,319
thing about art to do this. I'm not an artist myself and I did the experiment. You can check

65
00:05:24,319 --> 00:05:28,889
it out in a special bonus episode we have next. So why don't you try this out for yourself.

66
00:05:28,889 --> 00:05:33,560
Film it and upload it to us as a video response. Check this out, I even made a PDF of a body

67
00:05:33,560 --> 00:05:38,939
that you can use just for your experiment. Just the kind of guy I am! I'm Julian, and

68
00:05:38,939 --> 00:05:40,500
this has been The Science of Happiness.

69
00:05:40,500 --> 00:05:45,000
SoulPancake Subscribe!

'''

def call_llm():

    messages = [
        {'role': 'system', 'content': '你是一个视频srt字幕分析剪辑器，输入视频的srt字幕，分析其中的精彩且尽可能连续的片段并裁剪出来，输出的片段至少1分钟以上，但不要超过2分钟，将片段中在时间上连续的多个句子及它们的时间戳合并为一条，注意确保文字与时间戳的正确匹配。输出需严格按照如下格式：1. [开始时间-结束时间] 文本，注意其中的连接符是“-”。除了上述格式的字幕内容以外什么都不要输出。'},
        {'role': 'user', 'content': content}
        ]
    response = Generation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key="sk-14a27b1701374cf3a4c00e9897327467",
        model="qwen-plus",   # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages,
        result_format="message"
    )

    if response.status_code == 200:
        print(response.output.choices[0].message.content)
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")


if __name__ == '__main__':
    call_llm()