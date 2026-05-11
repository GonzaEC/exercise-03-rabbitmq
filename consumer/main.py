import json
import os
import time
import pika


def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"EVENT: {data['event']} | node: {data['node_name']} | time: {data['timestamp']}", flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    while True:
        try:
            params = pika.URLParameters(url)
            conn = pika.BlockingConnection(params)
            ch = conn.channel()
            ch.queue_declare(queue="node_events", durable=True)
            ch.basic_consume(queue="node_events", on_message_callback=callback)
            print("Consumer ready, waiting for events...", flush=True)
            ch.start_consuming()
        except Exception as e:
            print(f"Connection failed: {e}, retrying in 3s...", flush=True)
            time.sleep(3)


if __name__ == "__main__":
    main()
