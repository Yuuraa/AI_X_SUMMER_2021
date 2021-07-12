from kafka import KafkaProducer
import sys
import json

SERVER_IP = 'NUC의 IP를 설정해 주세요'
producer = KafkaProducer(bootstrap_servers=[f'{SERVER_IP}:9092'], value_serializer=lambda m: json.dumps(m).encode('utf-8'))
topic = 'chat'
content = 'Python으로 메시지 보내기~'
#content = 'python message'

k = 0
while True:
    try:
        content = {str(k): content}
        producer.send(topic, content)
        k += 1
        content = input('메시지를 입력하세요: ')
        #producer.poll()
    except BufferError:
        print(f"로컬 producer의 큐가 가득 찼습니다. ({len(producer)}개의 메시지들이 전송 대기중입니다): 다시 시도해주세요")
    except KeyboardInterrupt:
        print("메시지 전송을 종료합니다")
        break


producer.flush()




