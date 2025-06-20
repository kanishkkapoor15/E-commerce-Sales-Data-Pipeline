from kafka import KafkaConsumer
import json

# Configurations
MAX_MESSAGES = 10  # Read 10 messages and then stop

# Creating consumer
consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="order-consumers",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("🔄 Listening to Kafka topic: 'orders'...")

count = 0
for message in consumer:
    order = message.value

    print("🔹 Received order:", order["order_id"])
    print("   User ID:", order["user"]["user_id"])
    print("   Product:", order["product"]["name"])
    print("   Price:", order["product"]["price"])
    print("   Quantity:", order["quantity"])
    print("   Total:", order["total_price"])
    print("   Ordered at:", order["ordered_at"])
    print("-" * 50)

    count += 1
    if count >= MAX_MESSAGES:
        print(f"✅ Processed {MAX_MESSAGES} messages. Exiting.")
        break