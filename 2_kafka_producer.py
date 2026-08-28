import json
import time
import importlib
from kafka import KafkaProducer

# Import generate_order from Step 1 (1_generate_data.py)
generate_data = importlib.import_module("1_generate_data")
generate_order = generate_data.generate_order

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "sales_orders"


def create_producer():
    """Initializes and returns a KafkaProducer configured for JSON messages."""
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )


def send_orders(num_orders=10, delay_seconds=1):
    """Generates and sends sample sales orders to the Kafka topic."""
    producer = create_producer()
    print(f"Connected to Kafka broker at {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"Sending {num_orders} orders to topic '{KAFKA_TOPIC}'...\n")

    for i in range(1, num_orders + 1):
        order = generate_order(order_id=2000 + i)
        
        # Send message to Kafka topic
        producer.send(KAFKA_TOPIC, value=order)
        print(f"[Sent {i}/{num_orders}] Order ID: {order['order_id']} | Product: {order['product']} | Total: ${order['total_amount']}")
        
        # Short pause to simulate streaming
        time.sleep(delay_seconds)

    # Ensure all buffered messages are sent
    producer.flush()
    producer.close()
    print(f"\nSuccessfully sent {num_orders} orders to Kafka topic '{KAFKA_TOPIC}'!")


if __name__ == "__main__":
    try:
        send_orders(num_orders=10, delay_seconds=1)
    except Exception as e:
        print("\n[Error] Could not connect to Kafka broker.")
        print(f"Details: {e}")
        print("\nPlease make sure Kafka is running on localhost:9092 before running this script.")
