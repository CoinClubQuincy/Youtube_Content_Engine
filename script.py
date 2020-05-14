from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy.editor as mpe
import moviepy.video as mpv
from random import randint
from math import floor
#plug in API Key in client_secrets.json
import YouTubeAPI
import boto3
import botocore
import random
import os
import yaml
from requests import get
from json import loads
from mutagen.mp3 import MP3

word_list = ['understanding', 'great', 'playful', 'calm', 'loving', 'concerned', 'eager', 'impulsive', 'irritated', 'lousy', 'upset', 'incapable', 'insensitive', 'fearful', 'crushed', 'tearful', 'confident', 'gay', 'courageous', 'peaceful', 'considerate', 'affected', 'keen', 'free', 'enraged', 'disappointed', 'doubtful', 'alone', 'dull', 'terrified', 'tormented', 'sorrowful', 'reliable', 'joyous', 'energetic', 'at', 'ease', 'affectionate', 'fascinated', 'earnest', 'sure', 'hostile', 'discouraged', 'uncertain', 'paralyzed', 'nonchalant', 'suspicious', 'deprived', 'pained', 'easy', 'lucky', 'liberated', 'comfortable', 'sensitive', 'intrigued', 'intent', 'certain', 'insulting', 'ashamed', 'indecisive', 'fatigued', 'neutral', 'anxious', 'pained', 'grief', 'amazed', 'fortunate', 'optimistic', 'pleased', 'tender', 'absorbed', 'anxious', 'rebellious', 'sore', 'powerless', 'perplexed', 'useless', 'reserved', 'alarmed', 'tortured', 'anguish', 'free', 'delighted', 'provocative', 'encouraged', 'devoted', 'inquisitive', 'inspired', 'unique', 'annoyed', 'diminished', 'embarrassed', 'inferior', 'weary', 'panic', 'dejected', 'desolate', 'sympathetic', 'overjoyed', 'impulsive', 'clever', 'attracted', 'nosy', 'determined', 'dynamic', 'upset', 'guilty', 'hesitant', 'vulnerable', 'bored', 'nervous', 'rejected', 'desperate', 'interested', 'gleeful', 'free', 'surprised', 'passionate', 'snoopy', 'excited', 'tenacious', 'hateful', 'dissatisfied', 'shy', 'empty', 'preoccupied', 'scared', 'injured', 'pessimistic', 'satisfied', 'thankful', 'frisky', 'content', 'admiration', 'engrossed', 'enthusiastic', 'hardy', 'unpleasant', 'miserable', 'stupefied', 'forced', 'cold', 'worried', 'offended', 'unhappy', 'receptive', 'important', 'animated', 'quiet', 'warm', 'curious', 'bold', 'secure', 'offensive', 'detestable', 'disillusioned', 'hesitant', 'disinterested', 'frightened', 'afflicted', 'lonely', 'accepting', 'festive', 'spirited', 'certain', 'touched', 'brave', 'bitter', 'repugnant', 'unbelieving', 'despair', 'lifeless', 'timid', 'aching', 'grieved', 'kind', 'ecstatic', 'thrilled', 'relaxed', 'sympathy', 'daring', 'aggressive', 'despicable', 'skeptical', 'frustrated', 'shaky', 'victimized', 'mournful', 'satisfied', 'wonderful', 'serene', 'close', 'challenged', 'resentful', 'disgusting', 'distrustful', 'distressed', 'restless', 'heartbroken', 'dismayed', 'glad', 'free', 'and', 'easy', 'loved', 'optimistic', 'inflamed', 'abominable', 'misgiving', 'woeful', 'doubtful', 'agonized', 'cheerful', 'bright', 'comforted', 're-enforced', 'provoked', 'terrible', 'lost', 'pathetic', 'threatened', 'appalled', 'sunny', 'blessed', 'drawn', 'toward', 'confident', 'incensed', 'in', 'despair', 'unsure', 'tragic', 'cowardly', 'humiliated', 'merry', 'reassured', 'hopeful', 'infuriated', 'sulky', 'uneasy', 'in', 'a', 'stew', 'quaking', 'wronged', 'elated', 'cross', 'bad', 'pessimistic', 'dominated', 'menaced', 'alienated', 'jubilant', 'worked', 'up', 'a', 'sense', 'of', 'loss', 'tense', 'wary', 'boiling', 'fuming', 'indignant']

#--------------- Video Generator ---------------#
class Generator:

    def __init__(self, filename, audioname, MOV, OPACITY):
        self.total_duration = 0
        self.clip_list = []
        self.clip = mpe.VideoFileClip(filename)
        self.audio = mpe.AudioFileClip(audioname)
        self.overlay = mpe.VideoFileClip('%s' % MOV).subclip().resize(self.clip.size).set_opacity(OPACITY)

    def audi_test(self):
        f = self.clip.set_audio(self.audio)
        f.write_videofile('out.mp4', temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

    def create(self, desired_length, Color,OPACITY2):
        self.random_word_screen()
        while self.total_duration < desired_length:
            self.add_clip()
        final = mpe.concatenate_videoclips(self.clip_list)
        image = mpe.ImageClip('%s' % Color).resize(self.clip.size).set_opacity(OPACITY2).set_duration(self.total_duration)
        final = mpe.CompositeVideoClip([final, image])
        self.audio = self.audio.set_duration(self.total_duration)
        final = final.set_audio(self.audio)
        final.write_videofile('output_file.mp4', temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

    def add_clip(self):
        r = randint(0, floor(self.clip.duration-10))
        subclip = self.clip.subclip(r, r+(r%10))
        merged = mpe.CompositeVideoClip([subclip, self.overlay.subclip(2, 2+r%10)])
        if r%2==0: #adds a fade_in transition if r is even.
            merged = mpv.fx.all.fadein(merged, 3)
        self.clip_list.append(merged)
        self.total_duration += r%10

    def random_word_screen(self):
        response = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
        word = '{quoteText}'.format(**loads(response.text))
        spaced_word = ''.join([e for e in word])
        clip = mpe.TextClip(spaced_word, fontsize = 27, color = 'blue',size=self.clip.size,bg_color = 'white',method='caption',align='center').set_duration(7)
        self.clip_list.append(clip)
        self.total_duration += 1

    def ADD_Intro(self,File):
        clip1 = VideoFileClip(File)
        clip2 = VideoFileClip("VIDEO_FILE.mp4")
        final_clip = concatenate_videoclips([clip1,clip2])
        final_clip.write_videofile("VIDEO_FILE.mp4")
        print("Video files connected")
#---------------AWS&YouTube API Engine ---------------#

class Youtube:

    def __init__(self):
        print("------------[Engine Start]------------")

    def S3(self):
        #get files from s3
        AudioFile = []
        VideoFile = []
        OverVid = []
        OverColor = []

        with open('assets/Config.yaml', 'r') as f:
            doc = yaml.load(f)
            The_Bucket = doc["YoutubeEngine"]["S3Bucket"]


        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(The_Bucket)

        for object_summary in my_bucket.objects.filter(Prefix="Media/Audio/"):
            AudioFile.append(object_summary.key)
        for object_summary in my_bucket.objects.filter(Prefix="Media/Video/"):
            VideoFile.append(object_summary.key)
        for object_summary in my_bucket.objects.filter(Prefix="Media/overLay_Color/"):
            OverColor.append(object_summary.key)
        for object_summary in my_bucket.objects.filter(Prefix="Media/overLay_Vid/"):
            OverVid.append(object_summary.key)

        AudioFile = AudioFile[1:]
        VideoFile = VideoFile[1:]
        OverVid = OverVid[1:]
        OverColor = OverColor[1:]
        STREAM_OverVid_FILE = random.choice(OverVid)
        STREAM_OverColor_FILE = random.choice(OverColor)
        STREAM_VIDEO_FILE = random.choice(VideoFile)
        STREAM_AUDIO_FILE = random.choice(AudioFile)
        SINGLE_AUDIO =STREAM_AUDIO_FILE.replace("Media/Audio/", '')
        SINGLE_VIDEO =STREAM_VIDEO_FILE.replace("Media/Video/", '')
        SINGLE_Color_OVER = STREAM_OverColor_FILE.replace("Media/overLay_Color/", '')
        SINGLE_VID_OVER = STREAM_OverVid_FILE.replace("Media/overLay_Vid/", '')

        try:
            my_bucket.download_file(STREAM_AUDIO_FILE,'AUDIO_FILE.mp3')
            my_bucket.download_file(STREAM_VIDEO_FILE,'VIDEO_FILE.mp4')
            my_bucket.download_file(STREAM_OverVid_FILE,'VID_OVERLAY_FILE.mov')
            my_bucket.download_file(STREAM_OverColor_FILE,'COLOR_OVERLAY_FILE.png')

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

    def S3_Upload(self,Name):
        with open('assets/Config.yaml', 'r') as f:
            doc = yaml.load(f)
            my_bucket = doc["YoutubeEngine"]["S3Bucket"]

        s3 = boto3.resource('s3')
        bucket = s3.Bucket('mybucket')
        Name = Name.replace(" ", '' )
        Name = Name + ".mp4"
        print(Name)

        s3.meta.client.upload_file('output_file.mp4', my_bucket, 'Media/Outputs/%s' % Name)

    def YouTubeAPI(self,TITLE,DES,KW,Privacy):
        TITLE = '"%s"' % TITLE
        DES = '"%s"' % DES
        KW = '"%s"' % KW
        Privacy = '"%s"' % Privacy
        #[SCRIPT] python3 YouTubeAPI.py --file="output_file.mp4" --title="title" --description="info" --keywords="list" --privacyStatus="private"
        RunAPI = "--title=%s --description=%s --keywords=%s --privacyStatus=%s " % (TITLE, DES, KW,Privacy)
        os.system("python3 YouTubeAPI.py --file output_file.mp4 %s" % RunAPI)

        # upload copy to S3
    def AI_Config(self):
        print("test")

    def Engine(self):
        # Update all config files
        #1 Pull From S3
        print("---[Pull from S3]---")
        self.S3()

        print("---[Read Config file]---")
        #2 Read config
        with open('assets/Config.yaml', 'r') as f:
            doc = yaml.load(f)
            YT_Title = doc["YoutubeEngine"]["Title"]
            YT_DES = doc["YoutubeEngine"]["Description"]
            YT_KEYWORDS = doc["YoutubeEngine"]["Keywords"]
            desired_duration = doc["YoutubeEngine"]["VideoDuration"]

            video_intro =  doc["YoutubeEngine"]["VideoInt"]
            movie_name = doc["YoutubeEngine"]["Movie_name"]
            music = doc["YoutubeEngine"]["Music"]
            Color = doc["YoutubeEngine"]["Color"]
            Vid_overlay = doc["YoutubeEngine"]["Vid_overlay"]
            Privacy =  doc["YoutubeEngine"]["Stat"]

            OPACITY= doc["YoutubeEngine"]["Overlay_OPACITY"]
            OPACITY2 =  doc["YoutubeEngine"]["Color_OPACITY"]

            YT_Cycles = doc["YoutubeEngine"]["YT_Cycles"]
            S3_Cycles =  doc["YoutubeEngine"]["S3_Cycles"]

            # Set config file to Generate to generate title
            if YT_Title == "Generate":
                list =[]
                #open and read the file after the appending:

                f = open("assets/wlist.txt", "r")
                for i in f:
                    z= list.append(str(i))

                rand = random.choice(list)
                rand = rand.replace("\n", '')
                Name_Title= "%s %s " % (random.choice(word_list),rand)

                YT_Title = Name_Title

                if desired_duration == "Generate":
                    audio = MP3(music)
                    desired_duration = int(audio.info.length) - 3
                    print(audio.info.length)

            print(YT_Title, desired_duration)

        print("---[start generator]---")

        #3 start generator
        g = Generator(movie_name, music,Vid_overlay,OPACITY)
        g.create(desired_duration,Color,OPACITY2)


        if YT_Cycles != "skip":

            #5 upload yo youtube
            print("---[Upload to youtube]---")
            self.YouTubeAPI(YT_Title, YT_DES,YT_KEYWORDS,Privacy)
            print("---[Upload Copy to S3]---")
            self.S3_Upload(YT_Title)

            print("Start again")
            os.system("rm output_file.mp4")
            count += 1
            start = Youtube()


            print("complete")

        else:
            print("Youtube Skiped")
            self.S3_Upload(YT_Title)

            print("------------------- Video complete! -------------------")
            os.system("rm output_file.mp4")


if __name__ == '__main__':

    start = Youtube()
    start.Engine()

#
