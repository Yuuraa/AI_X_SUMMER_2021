import imutils
import argparse
import cv2
import os
import numpy as np

from style_transfer_functions import StyleTransferNet


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", default="../dataset/objects/dog_bicycle.jpg")
    parser.add_argument("--style_name", default="/home/yura/AI_X_SUMMER_2021/style_transfer/models/mosaic_light.onnx")
    args = parser.parse_args()

    model = StyleTransferNet(args.style_name)

    image_path = args.img_path
    img = cv2.imread(image_path)

    output = model.inference(img)

    # 원본 영상과 스타일 변환된 영상을 함께 출력합니다
    print("스타일 변환을 수행합니다. esc 키를 누르면 종료합니다")
    while True:
        cv2.imshow("Input", img)
        cv2.imshow("Output", output)

        if cv2.waitKey(1) > 0:
            break
    print("스타일 변환을 종료합니다")
        