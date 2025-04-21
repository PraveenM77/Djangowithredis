import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

while True:
    try:
        consumer = KafkaConsumer(
            'searchdata',  # Topic name
            bootstrap_servers='kafka:9092', 
            auto_offset_reset='earliest',
            group_id='search_group'
        )
        print("Kafka Consumer Connected!")

        # Keep listening
        for message in consumer:
            print(f"Received message: {message.value.decode('utf-8')}")

    except NoBrokersAvailable:
        print("Kafka broker not available, retrying in 5 seconds...")
        time.sleep(5)
    except Exception as e:
        print(f"Consumer Error: {str(e)}")
        time.sleep(5)
