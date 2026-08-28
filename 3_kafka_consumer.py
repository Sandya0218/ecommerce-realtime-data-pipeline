"""
Step 3: Kafka Consumer & Bronze Layer Storage
=============================================
Purpose:
  - Connects to the Kafka topic 'sales_orders'.
  - Consumes incoming raw JSON order messages.
  - Appends and stores the raw records directly into the Bronze layer (data/bronze/bronze_orders.json).
"""

import json
import os
from kafka import KafkaConsumer

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "sales_orders"

# Bronze Layer Storage Path
BRONZE_FILE_PATH = os.path.join("data", "bronze", "bronze_orders.json")


def create_consumer():
    """Initializes and returns a KafkaConsumer for JSON messages."""
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        auto_offset_reset="earliest",       # Read from beginning if no offset is committed
        enable_auto_commit=True,
        group_id="bronze_consumer_group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        consumer_timeout_ms=10000          # Closes cleanly if no new messages arrive for 10s
    )


def consume_and_save_to_bronze():
    """Consumes messages from Kafka and writes them to the Bronze storage file."""
    # Ensure the bronze folder exists
    os.makedirs(os.path.dirname(BRONZE_FILE_PATH), exist_ok=True)

    print(f"Connecting to Kafka topic '{KAFKA_TOPIC}'...")
    consumer = create_consumer()
    print(f"Listening for messages... (Saving to '{BRONZE_FILE_PATH}')\n")

    message_count = 0

    # Append incoming raw JSON messages into bronze file (JSON Lines format)
    with open(BRONZE_FILE_PATH, "a", encoding="utf-8") as file:
        for message in consumer:
            order = message.value
            file.write(json.dumps(order) + "\n")
            message_count += 1
            print(f"[Bronze Saved #{message_count}] Order ID: {order['order_id']} | Product: {order['product']} | Total: ${order['total_amount']}")

    consumer.close()

    if message_count > 0:
        print(f"\n[SUCCESS] Saved {message_count} raw order(s) to Bronze layer: '{BRONZE_FILE_PATH}'")
    else:
        print("\n[NOTICE] No new messages received from Kafka within timeout.")


if __name__ == "__main__":
    try:
        consume_and_save_to_bronze()
    except Exception as e:
        print("\n[Error] Could not connect or consume from Kafka.")
        print(f"Details: {e}")
        print("\nPlease ensure Kafka is running on localhost:9092.")
