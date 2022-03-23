"""RabbitMQ reception server for API_Vbox

@author Rxinui
@date 2022-03-03
"""
import os
import sys
import json
import subprocess
from typing import List
import pika
from utils import logger
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from dotenv import load_dotenv

load_dotenv(".api_vbox.env")
logger = logger(__file__, f"{__file__}.log")
USERS_REQUEST_QUEUE = os.environ["API_VBOX_USERS_REQUEST_QUEUE"]


def _execute_cmd(cmd: List[str]) -> str:
    """Execute a shell command.

    Args:
        cmd (List[str]): command

    Returns:
        str: command output
    """
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        return proc.communicate()[0].decode("utf-8")


def on_request(
    ch: BlockingChannel,
    method: Basic.Deliver,
    props: BasicProperties,
    body: bytes,
):
    """Callback triggered on request from the api_vbox's user.

    Args:
        ch (BlockingChannel): _description_
        method (Basic.Deliver): _description_
        props (BasicProperties): _description_
        body (bytes): _description_
    """
    response = json.loads(body)
    message = "on_request@user#%s: exec '%s'"
    print(message %( response["client_id"], response["req"]))
    logger.info(message, response["client_id"], response["req"])
    response["res"] = {}
    response["res"]["output"] = _execute_cmd(response["req"]["cmd"])
    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,  # REPLY_QUEUE defined by Client
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id,
            content_type="application/json",
            content_encoding="utf-8",
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
    logger.info("main: channel %s declared and ready to consume", USERS_REQUEST_QUEUE)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=USERS_REQUEST_QUEUE, on_message_callback=on_request)
    try:
        print(
            f"Waiting for messages on {USERS_REQUEST_QUEUE}. Press Ctrl+C to exit...\r"
        )
        channel.start_consuming()
    except KeyboardInterrupt:
        if connection.is_open:
            connection.close()
        sys.exit(0)
    sys.exit(1)
