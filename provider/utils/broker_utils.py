import json
import socket

import pika

from db import base, crud
from sqlmodel import Session

# Configuration
EXCHANGE_NAME = "ds_file_exchange"
ROUTING_KEY = "route_general"
CONNECTION_PARAMETERS = pika.ConnectionParameters(host=socket.gethostbyname("broker"))


# Define callback function for received messages
def on_message(ch, method, properties, body):
    try:
        data = json.loads(body.decode())
        file_uid = data.get('file_uid')
        token = data.get('token')
        with Session(base.engine) as session:
            crud.add_token(session, file_uid, token)
    except json.JSONDecodeError:
        print("Invalid JSON format")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def setup_consumer():
    connection = pika.BlockingConnection(CONNECTION_PARAMETERS)
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=ROUTING_KEY)
    channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=False)
    channel.start_consuming()

# if __name__ == '__main__':
#     setup_consumer()
