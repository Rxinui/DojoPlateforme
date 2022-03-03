"""RabbitMQ reception server for API_Vbox

@author Rxinui
@date 2022-03-03
"""
import os
import sys
import json
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from lib import get_logger, INFO
from dotenv import load_dotenv

load_dotenv(".api_vbox.env")
logger = get_logger(__file__, f"{__file__}.log", level=INFO)
USERS_REQUEST_QUEUE = os.environ["API_VBOX_USERS_REQUEST_QUEUE"]


def __on_request(
    ch: BlockingChannel,
    method: Basic.Deliver,
    props: BasicProperties,
    body: bytes,
):
    """Callback triggered on request from the api_vbox's user.

    Args:
        ch (_type_): _description_
        method (_type_): _description_
        props (_type_): _description_
        body (_type_): _description_
    """
    response = json.loads(body)
    logger.info("on_request@user#%s", response["client_id"])
    logger.info("debug: %s", type(ch))
    response["res"] = "Success!!"
    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,  # REPLY_QUEUE defined by Client
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id, content_type="application/json"
        ),
        body=json.dumps(response),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            os.environ["API_VBOX_RABBITMQ_HOST"], os.environ["API_VBOX_RABBITMQ_PORT"]
        )
    )
    logger.info("main: connection established")
    channel = connection.channel()
    channel.queue_declare(queue=USERS_REQUEST_QUEUE)
    logger.info(
        "on_channel_open: channel %s declared and ready to consume", USERS_REQUEST_QUEUE
    )
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=USERS_REQUEST_QUEUE, on_message_callback=__on_request)
    try:
        print("Waiting for messages. Press Ctrl+C to exit...")
        channel.start_consuming()
    except KeyboardInterrupt:
        if connection.is_open:
            connection.close()
        sys.exit(0)
    sys.exit(1)
