import os
import sys
import unittest
from pathlib import Path
from typing import List

from core.utils.video import video_split
from core.utils.video.video_split import time_str_to_seconds

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))


llm_response = """
[00:00:25,500-00:01:58,299] Julian: Art, the expression or application of human creative skill and imagination. That is how it is defined in the dictionary of my Macbook. You probably heard the term art therapy thrown around before but today we're honing on a new type of art therapy designed exclusively to focus in on positive emotions, personal control, and a sense of meaning. Now you can get the down low on it here, but full disclosure, watching us test it out ourselves is gonna be more entertaining. Plus, I have my own art therapist! Pamela: Hey how are you doing? Julian: I'm good, I'm good, how are you? Pamela: I'm good Julian: Great! Welcome. Pamela is a registered and board certified art therapist with the American Art Therapy Association. So, can flexing your artistic muscles really make you happier? Let's find out! Once again we brought in a selection of subjects. Now first we gave them a test to measure their current level of happiness. Participant 3: I nailed it! Julian: You're not done yet, no there's more. Next we asked them to write a list of things in their life that made them feel happier or supported. Then we had them assign a color to themselves and each of the things on their list. P3: I'm just gonna write ladies. Pamela: [laughs] That works. Julian: I don't think there's any misinterpreting that. It felt like the right time to rope them into doing something creative, so we traced a life-sized outline of their body, and told them to fill it in with the different colors depending on where it resonated for them. We told them to put a circle in the center that represented themselves. Now they hadn't realized it, but we put them in a reflective state of mind and in order to complete the exercise, they had to really focus on how each person or thing contributed to their life.
[00:02:05,549-00:03:38,879] Pamela: So, what was that like for you? Participant 4: Oh I loved it! I love art and I love to paint, I used to paint when I was a little girl with my grandma. Pamela: Oh you did? P4: I just think about my grandma a lot. She taught me how to paint. Pamela: I noticed the first thing you put in there was the purple to represent, is that mom? Participant 5: My mom, yeah, she's like on the shoulder kinda area I guess? My mom actually, I remember when she used to rub my shoulders whenever I would be sick as a kid. Pamela: Out of all of these things, what are you most passionate about? Participant 6: Um, well of course my family. I have seven children and they're spread all over. There are three in California and I rarely get to see them, so I have to say that my family is my passion. Pamela: Orange, what is orange? P3: Orange is ladies. Pamela: The ladies. P3: Yeah, I've always had an interesting relationship with women over the course of my life. When I was young, I was always the class clown and it was always difficult for me to connect with women because they wanted a serious man in their life but I was always trying to make them laugh. So they were always unattainable presence in my life. Like I was never able to have a girlfriend when I was a kid so, I feel like that has always been a hurdle that needs to be dealt with. Pamela: Right. P3: So when you look at me you just see wow that man is very emotional and very passionate about a plethora of different things. P2: I see a paint representation of my personality.
[00:03:40,519-00:04:53,080] Pamela: The first thing you put on here was your dad. P3: My dad has always been the one that's been there my whole life. I'm a daddy's girl for sure. Pamela: How is he there for you? P3: My gosh, I have to be careful what I say around him. Like, when I say "I broke my pencil today" I'll have 24 packs of pencils on my doorstep the next day. Every time I'm on the phone with my dad present day, he's like, "well just in case I'm not around tomorrow" you know, stuff like that. Pamela: Is that hard sometimes for you, when he makes a joke out of something so big. P3: Yes, but it's just like that. P1: The one right in the middle, um, is my mom. What is going on? This is so weird! [laughs] Yeah, cause I think just looking at this, you know she really is like my core. She's like the foundation upon which everything else is kind of been built upon, so she's been the example through that kind of guides me to even be able to assess where everything lies so my mom, yeah. Julian: So, what did we find out. Well, we saw an average increase in happiness 8.1% with the highest just being 36.7%.
[00:04:59,879-00:05:40,500] Well, Picasso once said, "Art washes away from the soul the dust of everyday life" and I am starting to think that dude was on to something. When you engage yourself artistically and use your imagination, you can help regulate your blood pressure and your heart rate. Now I know what you're thinking. I'm not an artist. Well don't worry, you don't need to know a thing about art to do this. I'm not an artist myself and I did the experiment. You can check it out in a special bonus episode we have next. So why don't you try this out for yourself. Film it and upload it to us as a video response. Check this out, I even made a PDF of a body that you can use just for your experiment. Just the kind of guy I am! I'm Julian, and this has been The Science of Happiness.
"""


# 从llm_response中截取时间范围，并转换成时间范围元组。
def get_time_ranges(llm_response: str) -> List[tuple]:
    time_ranges = []
    for line in llm_response.split('\n'):
        if '[' in line and ']' in line:
            line = line.split(" ")[0]
            start_time, end_time = line[1:-1].split('-')
            # 00:00:25,500 格式转换成秒，保留两位小数
            start_time_value = time_str_to_seconds(start_time.strip())
            end_time_value = time_str_to_seconds(end_time.strip())
            time_ranges.append((start_time_value, end_time_value))
    return time_ranges


class VideoSpiltTest(unittest.TestCase):

    def test_detect_scene_and_spilt(self):
        video_path = os.path.join(project_root, "file/output", "v1_with_subtitle.mp4")
        # video_path = os.path.join(project_root, "file", "v1_mixed.mp4")
        output_dir = os.path.join(project_root, "file/spilt")
        video_split.detect_scene_and_spilt(video_path, output_dir, threshold=30, min_duration=60)


    def test_video_split_v2(self):
        video_path = os.path.join(project_root, "file/output", "v1_with_subtitle.mp4")
        output_dir = os.path.join(project_root, "file/spilt")
        video_split.split_video_v2(video_path, output_dir, get_time_ranges(llm_response))
