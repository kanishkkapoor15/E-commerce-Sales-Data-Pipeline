import requests
import json
from kafka import KafkaProducer
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

API_URL = "http://localhost:8000/orders?count=5"

def fetch_orders():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch from API:", response.status_code)
        return []

def send_to_kafka(orders):
    for order in orders:
        producer.send("orders", value=order)
        print("✅ Sent to Kafka:", order["order_id"])
    producer.flush()

if __name__ == "__main__":
    num_batches = 3  # Send 3 batches
    for _ in range(num_batches):
        orders = fetch_orders()
        if orders:
            send_to_kafka(orders)
        time.sleep(15)  # Wait before next batch

    print("✅ Done producing messages.")