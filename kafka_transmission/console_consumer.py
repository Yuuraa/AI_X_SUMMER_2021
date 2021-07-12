from kafka import KafkaConsumer
from kafka.errors import KafkaError


SERVER_IP = '서버 ip를 지정하세요'
topic = 'chat'
consumer=KafkaConsumer(topic, bootstrap_servers=[f'{SERVER_IP}:9092'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"Topic {topic}의 메시지 파티션의 오프셋의 끝에 도달했습니다")
            else:
                print("에러가 발생했습니다")
                break
        else:
            print(f"도착한 메시지: {msg.value()}")
        
except KeyboardInterrupt:
    print("수신을 마칩니다")

consumer.close()