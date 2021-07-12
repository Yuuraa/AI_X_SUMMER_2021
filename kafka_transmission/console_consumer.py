from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json
import configparser


config = configparser.ConfigParser()
config.read('./config.conf')
server_ip = config.get('Broker', 'SERVER_IP')
topic = config.get('Broker', 'TOPIC')

consumer=KafkaConsumer(topic, bootstrap_servers=[f'{server_ip}:9092'], value_deserializer=lambda m: json.loads(m.decode('utf-8')))

try:
    for msg in consumer:
        print(f"도착한 메시지: {msg.value}")
        
except KeyboardInterrupt:
    print("수신을 마칩니다")

consumer.close()
