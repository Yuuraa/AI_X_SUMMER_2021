from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json


SERVER_IP = 'NUC의 IP 주소를 입력하세요'
topic = 'chat'
consumer=KafkaConsumer(topic, bootstrap_servers=[f'{SERVER_IP}:9092'], value_deserializer=lambda m: json.loads(m.decode('utf-8')))

try:
    for msg in consumer:
        #msg = consumer.poll(timeout=1.0)
        #if msg is None:
        #    continue
        #if msg.error():
        #    if msg.error().code() == KafkaError._PARTITION_EOF:
         #       print(f"Topic {topic}의 메시지 파티션의 오프셋의 끝에 도달했습니다")
          #  else:
           #     print("에러가 발생했습니다")
            #    break
        #else:
        print(f"도착한 메시지: {msg.value}")
        
except KeyboardInterrupt:
    print("수신을 마칩니다")

consumer.close()
