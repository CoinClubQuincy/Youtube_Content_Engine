from pydub import AudioSegment
from pydub.playback import play
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

class Test:

    def test1(self):
        #pip3 install pydub
        sound1 = AudioSegment.from_mp3("file1.mp3")
        sound2 = AudioSegment.from_mp3("file1.mp3")

        # mix sound2 with sound1, starting at 5000ms into sound1)
        output = sound1.overlay(sound2, position=50)

        # save the result
        output.export("mixed_sounds.mp3", format="mp3")

    def test2(self,start_time,end_time):
        ffmpeg_extract_subclip("video1.mp4", start_time, end_time, targetname="test.mp4")
        print("test")

    def test3(self,start,end):
        clip = VideoFileClip("SoFoIntro.mp4").subclip(start, end)
        clip.to_videofile(outputfile, codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')

if __name__ == '__main__':

    start = Test()
    start.test3(0,3)
