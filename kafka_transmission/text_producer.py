from kafka import KafkaConsumer

SERVER_IP = '서버 ip를 지정하세요'
consumer=KafkaConsumer('chat', bootstrap_servers=[f'{SERVER_IP}:9092'])

def print_msg():
    for message in consumer:
        print(message)

print_stream()