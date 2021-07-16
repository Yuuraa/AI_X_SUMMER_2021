import pafy
import cv2

# Youtube의 동영상 스트림을 받아오는 클래스입니다
class YoutubeStream:
    def __init__(self, url="https://youtu.be/YLXfyHsfFz0"):
        self.url = url
        self.youtube_video = self.get_video(url)
    
    def get_video(self, url):
        video = pafy.new(url)
        best = video.getbest(preftype="mp4")
        video = cv2.VideoCapture(best.url) 
        return video
    
    def get_stream(self):
        while True:
            ret, frame = self.youtube_video.read()
            yield ret, frame