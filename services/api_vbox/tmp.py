"""RabbitMQ reception client test for API_Vbox

@author Rxinui
@date 2022-03-03
"""
import uuid
import json
import sys
import os
import pika
import pika.channel
from lib import get_logger, INFO
from dotenv import load_dotenv

load_dotenv(".env")
logger = get_logger(__file__, f"{__file__}.log", level=INFO)


class RPCClient:
    USERS_REQUEST_QUEUE = os.environ["API_VBOX_USERS_REQUEST_QUEUE"]
    REPLY_WAITING_TIME_LIMIT = 10

    def __init__(self, client_id: str):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ["API_VBOX_RABBITMQ_HOST"],
                port=os.environ["API_VBOX_RABBITMQ_PORT"],
            )
        )
        self.channel = self.connection.channel()
        self.client_id = client_id
        # STEP 1.bis: declare REPLY_USER_QUEUE with a unique random id
        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def on_response(self, ch, method, props, body):
        # cb method called when server is replying
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, value):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        request_body = dict(client_id=self.client_id, req=msg)

        # STEP 2: publish message within the queue
        self.channel.basic_publish(
            exchange="",
            routing_key=self.USERS_REQUEST_QUEUE,  # QUEUE to publish
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,  # QUEUE that will be used to reply
                correlation_id=self.corr_id,  # request's unique ID
                content_type="application/json",
            ),
            body=json.dumps(request_body),
        )
        self.connection.process_data_events(time_limit=self.REPLY_WAITING_TIME_LIMIT)
        return self.response


if __name__ == "__main__":
    try:
        client = RPCClient(sys.argv[1])
        msg = input("msg: ")
        response = client.call(msg)
        if response:
            print(json.loads(response))
            sys.exit(0)
        else:
            print("***** The server does not reply.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
