from kafka import KafkaProducer
from kafka.errors import KafkaError
import subprocess as sub

SERVER_IP = '서버 ip를 지정하세요'
producer = KafkaProducer(bootstrap_servers=[f'{SERVER_IP}:9092'])
topic = 'chat'
content = 'Python으로 메시지 보내기~'

def transmit_kafka():
    while True:
        producer.send(topic, content)
        content = input('메시지를 입력하세요: ')

transmit_kafka()



