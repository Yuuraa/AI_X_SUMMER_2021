from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import time

from kafka import KafkaConsumer


# 
def show_raw_detection(image, detector, predictor):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
            
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(image, f"Face #{i+1}", (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        for (x, y) in shape:
            cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

    return image


def draw_individual_detections(image, detector, predictor):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
            clone = image.copy()
            cv2.putText(clone, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            for (x, y) in shape[i:j]:
                cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)

        (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))

        roi = image[y:y+h, x:x+w]
        roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)

        cv2.imshow("ROI", roi)
        cv2.imshow("Image", clone)
        cv2.waitKey(0)

        output = face_utils.visualize_facial_landmarks(image, shape)
        cv2.imshow("Image", output)
        cv2.waitKey(0)


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


if __name__ == "__main__":
    import configparser

    config = configparser.ConfigParser()
    config.read('./config.conf')
    server_ip = config.get('Broker', 'SERVER_IP')
    topic = config.get('Broker', 'TOPIC')

    consumer = KafkaConsumer(topic, bootstrap_servers=f"{server_ip}:9092")
    
    for message in consumer:
        array = np.frombuffer(message.value, dtype=np.dtype('uint8'))
        image = cv2.imdecode(array, 1)
        image = imutils.resize(image, width=500) # TODO: 이 resize 반드시 필요할지..?

        img = show_raw_detection(image, detector, predictor)
        cv2.imshow("Output", img)

        if cv2.waitKey(1) > 0:
            break

    print("얼굴 특징점 추출을 종료합니다")