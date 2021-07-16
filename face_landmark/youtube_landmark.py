from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import time
import os
import argparse

from landmark_utils import show_raw_landmarks, show_landmark_shape
import pafy


# Youtube의 동영상 스트림을 받아오는 클래스입니다
class YoutubeStream:
    def __init__(self, url):
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


if __name__ == "__main__":
    # 인자로 데이터의 경로를 받습니다
    parser = argparse.ArgumentParser()
    parser.add_argument("--show_parts", type=bool, default=False)
    parser.add_argument("--youtube_url", type=str, default="https://youtu.be/YLXfyHsfFz0")
    args = parser.parse_args()

    # 얼굴 탐지기(detector)와 특징점 추출기(predictor)를 선언합니다
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    
    # 유튜브 동영상을 생성합니다
    video = YoutubeStream(args.youtube_url)

    print("이미지 창에서 esc 버튼을 눌러 종료하세요. 얼굴 특징점 추출을 시작합니다")
    for ret, frame in video.get_stream():
        if not ret:
            print("비디오를 가져오는 중 오류가 발생했습니다")
            break

        image = imutils.resize(frame, width=500)
        show_landmark_shape(image, detector, predictor) # 동영상 내 사람 얼굴을 탐지하고 보여줍니다

        if cv2.waitKey(1) > 0:
            break

    print("얼굴 특징점 추출을 종료합니다")