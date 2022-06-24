"""RabbitMQ reception server for API_Vbox

@author Rxinui
@date 2022-03-03
"""
import os
import sys
import json
import subprocess
import logging
from typing import List, Tuple
from pathlib import Path
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from dotenv import load_dotenv

# Global constants
FILE_REALPATH = Path(os.path.realpath(__file__))
GLOBAL_ENV_PATH = FILE_REALPATH.parents[1]
LOGFILE = Path(f"/var/log/{FILE_REALPATH.name}.log")
LOGLEVEL = logging.INFO
EXEC_TIMEOUT = 300
EXIT_TIMEOUT_EXPIRED = -1000

"""Global setup

Initialize:
- load .env file
- program logger
"""
try:
    handler = logging.FileHandler(LOGFILE, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s::%(name)s::%(levelname)s::%(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(LOGLEVEL)
except PermissionError as exc:
    print(f"{exc.strerror}: '{LOGFILE}'", file=sys.stderr)
    print(
        f"Please, user '{os.getenv('USER')}' needs write permission \
        to {LOGFILE.parent}/ directory.",
        file=sys.stderr,
    )
    print(
        f"This script must be executed by a user \
        that has access to {os.getenv('STORAGE_VMS_BASEFOLDER')}.",
        file=sys.stderr,
    )
    sys.exit(exc.errno)

logger.info("Load .env file from '%s'", GLOBAL_ENV_PATH)
load_dotenv(GLOBAL_ENV_PATH / ".env")

# Global variables
USERS_REQUEST_QUEUE = os.environ["API_VBOX_USERS_REQUEST_QUEUE"]


def _execute_cmd(cmd: List[str]) -> Tuple[str, str, int]:
    """Execute a shell command.

    Args:
        cmd (List[str]): command

    Returns:
        str: command output
    """
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        try:
            output, error = proc.communicate(timeout=EXEC_TIMEOUT)
            output, error, exit_code = (
                output.decode("utf-8"),
                error.decode("utf-8"),
                proc.returncode,
            )
        except subprocess.TimeoutExpired:
            proc.kill()
            output, error, exit_code = (
                "",
                "subprocess timeout expired.",
                EXIT_TIMEOUT_EXPIRED,
            )

        return output, error, exit_code


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
    print(message % (response["client_id"], response["req"]))
    logger.info(message, response["client_id"], response["req"])
    response["res"] = {}
    (
        response["res"]["output"],
        response["res"]["error"],
        response["res"]["exit_code"],
    ) = _execute_cmd(response["req"]["cmd"])
    logger.info(response["res"])
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
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                os.environ["RABBITMQ_HOST"], os.environ["RABBITMQ_PORT"]
            )
        )
        logger.info("main: connection established")
        channel = connection.channel()
        channel.queue_declare(queue=USERS_REQUEST_QUEUE)
        logger.info(
            "main: channel %s declared and ready to consume", USERS_REQUEST_QUEUE
        )
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=USERS_REQUEST_QUEUE, on_message_callback=on_request)
        print(
            f"Waiting for messages on {USERS_REQUEST_QUEUE}. Press Ctrl+C to exit...\r"
        )
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as exc:
        logger.error(
            "RabbitMQ server %s:%s is unreachable.",
            os.environ["RABBITMQ_HOST"],
            os.environ["RABBITMQ_PORT"],
        )
        sys.exit(1)
    except KeyboardInterrupt:
        if connection.is_open:
            connection.close()
        sys.exit(1)
    sys.exit(0)
