import time
import sys
import configparser
import cv2

from kafka import KafkaProducer
from kafka.errors import KafkaError


# Broker 서버의 IP 주소와 사용할 topic 설정을 읽어옵니다
config = configparser.ConfigParser()
config.read("./config.conf")
server_ip = config.get('Broker', 'SERVER_IP')
topic = config.get('Broker', 'TOPIC')

# Kafka Producer를 선언합니다
producer = KafkaProducer(bootstrap_servers=f'{server_ip}:9092')

# 카메라 입력으로부터 계속해서 이미지를 생성합니다
def produce_videostream(device_path):
	print("비디오 전송을 시작합니다")
	video = cv2.VideoCapture(device_path)
	
	# 비디오를 읽어옵니다	
	while video.isOpened():
		success, frame = video.read()
		if not success: 
			break

		# 이미지 파일을 전송하기 위해 바이트로 인코딩합니다
		data = cv2.imencode('.jpeg', frame)[1].tobytes()

		# 이미지 데이터를 전송합니다
		future = producer.send(topic, data)
		try:
			future.get(timeout=10)
		except KafkaError as e:
			print(e)
			break
		print('.', end='', flush=True)


produce_videostream(0)
# 0 번째 카메라 장치를 사용합니다
