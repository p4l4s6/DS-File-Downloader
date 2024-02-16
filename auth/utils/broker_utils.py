import json
import socket

import pika

# Configuration
EXCHANGE_NAME = "ds_file_exchange"
ROUTING_KEY = "route_general"
CONNECTION_PARAMETERS = pika.ConnectionParameters(host=socket.gethostbyname("broker"))


def publish_event(event_data):
    connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)
    channel.confirm_delivery()
    try:
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=ROUTING_KEY,
            body=json.dumps(event_data),
            properties=pika.BasicProperties(delivery_mode=2)
        )
    finally:
        channel.connection.close()
