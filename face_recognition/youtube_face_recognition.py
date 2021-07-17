import argparse
import cv2
import imutils
import numpy as np
import os

from recognition_functions import get_known_encodings, detect_faces, recognize_faces, draw_recognition_results
import sys
sys.path.insert(0, '../utils')
from youtube_video import YoutubeStream


if __name__ == "__main__":   
    parser = argparse.ArgumentParser()
    parser.add_argument("--known_path", default="../dataset/single_face")
    parser.add_argument("--save_path", default="../dataset/single_face/saved_encodings.pkl")
    parser.add_argument("--threshold", type=float, default=0.6)
    parser.add_argument("--youtube_url", type=str, default="https://youtu.be/YLXfyHsfFz0")
    args = parser.parse_args()

    # 유튜브 동영상을 생성합니다
    video = YoutubeStream(args.youtube_url)
    
    # 미리 알고 있던 얼굴에 대한 정보를 불러옵니다
    known_names, known_encodings = get_known_encodings(args.known_path)
    
    print("얼굴 인식을 시작합니다. 이미지 창에서 esc 버튼을 누르면 종료합니다.")
    for ret, frame in video.get_stream():
        if not ret:
            print("비디오를 가져오는 중 오류가 발생했습니다")
            break
        img = imutils.resize(frame, width=500)

        face_locations = detect_faces(img)
        recognized_names = recognize_faces(img, face_locations, known_encodings, known_names, args.threshold)
        draw_recognition_results(img, face_locations, recognized_names)

        if cv2.waitKey(1) > 0:
            break
    
    print("얼굴 인식을 종료합니다")