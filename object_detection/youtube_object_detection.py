import os
import argparse
import cv2
import numpy as np

from object_detection_functions import YOLOModel, read_classes, show_detected_objects
import sys
sys.path.insert(0, '../utils')
from youtube_video import YoutubeStream


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weight_path", type=str, default="./yolov3-tiny.weights")
    parser.add_argument("--cfg_path", type=str, default="./yolov3-tiny.cfg")
    parser.add_argument("--class_path", type=str, default="./coco.names")
    parser.add_argument("--youtube_url", type=str, default="https://youtu.be/WriuvU1rXkc?t=22")
    args = parser.parse_args()

    # Model 정의
    print("모델을 로딩합니다... ")
    model = YOLOModel(args.weight_path, args.cfg_path)
    print("모델 로딩이 완료되었습니다")

    # 유튜브 동영상을 생성합니다
    video = YoutubeStream(args.youtube_url)
    classes = read_classes(args.class_path)
    
    print("객체 검출을 시작합니다. 이미지 창에서 esc 버튼을 누르면 종료합니다.")
    for ret, frame in video.get_stream():
        if not ret:
            print("비디오를 가져오는 중 오류가 발생했습니다")
            break
        
        cv2.imshow("Original Video", frame)

        outs = model.inference(frame)
        show_detected_objects(frame, outs, classes, threshold=0.4)

        if cv2.waitKey(1) > 0:
            break

    print("객체 검출을 종료합니다")