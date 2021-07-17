import imutils
import argparse
import time
import cv2
import os
import numpy as np

from style_transfer_functions import StyleTransferNet
from kafka import KafkaConsumer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="pi-video")
    parser.add_argument("--model_name", default="/home/yura/AI_X_SUMMER_2021/style_transfer/models/mosaic_light.onnx")
    args = parser.parse_args()

    model = StyleTransferNet(args.model_name)

    server_ip = os.environ.get("SERVER_IP")
    consumer = KafkaConsumer(args.topic, bootstrap_servers=f"{server_ip}:9092")

    
    print("스타일 변환을 수행합니다. esc 키를 누르면 종료합니다")
    SKIP_RATIO = 10 # 추론하는 데 시간이 오래 걸리기 때문에, 영상을 스킵하며 추론하도록 했습니다
    for i, message in enumerate(consumer):
        array = np.frombuffer(message.value, dtype=np.dtype('uint8'))
        img = cv2.imdecode(array, 1)
        
        if i % SKIP_RATIO == 0:
            output = model.inference(img)

        # 원본 영상과 스타일 변환된 영상을 함께 출력합니다
        cv2.imshow("Input", img)
        cv2.imshow("Output", output)

        if cv2.waitKey(1) > 0:
            break
    
    print("스타일 변환을 종료합니다")
        