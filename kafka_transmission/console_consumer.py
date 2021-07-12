# 사용할 라이브러리를 불러옵니다
from kafka import KafkaConsumer # kafka는 pip3로 설치한 kafka-python 라이브러리입니다. Consumer를 선언하기 위해 사용합니다
import json # json은 JSON 형식의 파일을 다룰 때 사용하고, 여기에서는 메시지를 JSON 형식으로 읽기 위해 사용합니다.
import configparser # configparser는 외부 파일에 설정값을 저장하고 사용하기 위해 사용됩니다

# config.conf 파일에서 server(broker)의 ip주소와 발행할 topic을 읽어옵니다
config = configparser.ConfigParser()
config.read('./config.conf')
server_ip = config.get('Broker', 'SERVER_IP')
topic = config.get('Broker', 'TOPIC')

# kafka-python 라이브러리에서 가져온 KafkaConsumer를 사용해 JSON 형식의 메시지를 받는 Kafka consumer를 정의합니다
consumer=KafkaConsumer(topic, bootstrap_servers=[f'{server_ip}:9092'], value_deserializer=lambda m: json.loads(m.decode('utf-8')))

# 사용자가 프로그램을 ctrl + C로 종료하기 전에는 계속해서 메시지를 받아옵니다
try:
    for msg in consumer:
        print(f"도착한 메시지: {msg.value}")
        
except KeyboardInterrupt:
    print("수신을 마칩니다")

consumer.close()
