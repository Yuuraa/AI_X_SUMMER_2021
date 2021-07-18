import imutils
import argparse
import time
import cv2
import os
import numpy as np

import sys
sys.path.insert(0, '../utils')
from youtube_video import YoutubeStream
from style_transfer_functions import StyleTransferNet


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--youtube_url", type=str, default="https://youtu.be/YLXfyHsfFz0")
    parser.add_argument("--style_path", default="/home/yura/AI_X_SUMMER_2021/style_transfer/models/mosaic_light.onnx")
    parser.add_argument("--skip_ratio", type=int, default=10)
    args = parser.parse_args()

    # 모델으르 정의합니다
    model = StyleTransferNet(args.style_path)

    # 유튜브 동영상을 생성합니다
    video = YoutubeStream(args.youtube_url)

    SKIP_RATIO = args.skip_ratio # 추론하는 데 시간이 오래 걸리기 때문에, 프레임을 스킵하며 추론하도록 했습니다
    print("스타일 변환을 수행합니다. esc 키를 누르면 종료합니다")
    for i, (ret, frame) in enumerate(video.get_stream()):
        if not ret:
            print("비디오를 가져오는 중 오류가 발생했습니다")
            break
        
        if i % SKIP_RATIO == 0:
            output = model.inference(frame)

        # 원본 영상과 스타일 변환된 영상을 함께 출력합니다
        cv2.imshow("Input", frame)
        cv2.imshow("Output", output)

        if cv2.waitKey(1) > 0:
            break
    
    print("스타일 변환을 종료합니다")