"""RPC Client designed for API_Vbox on a RabbitMQ broker.

@author Rxinui
@date 2022-03-03
"""

import uuid
import json
import os
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


class RPCClient:
    """RPC Client on RabbitMQ"""

    REPLY_WAITING_SECONDS_LIMIT = 10

    def __init__(self, client_id: str, request_queue: str):
        """Initialize a RPC client to communicate with RabbitMQ broker.

        Args:
            id (str): client id represented by the user id
        """
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ["API_VBOX_RABBITMQ_HOST"],
                port=os.environ["API_VBOX_RABBITMQ_PORT"],
            )
        )
        self.__channel = self.__connection.channel()
        self.__id = client_id
        self.request_queue = request_queue
        # STEP 1.bis: declare a private queue USER_REPLY_QUEUE with a unique random id
        result = self.__channel.queue_declare(
            queue=f"api_vbox.user#{self.__id}.reply_queue", exclusive=True
        )
        self.reply_queue = result.method.queue
        self.__channel.basic_consume(
            queue=self.reply_queue,
            on_message_callback=self.__on_response,
            auto_ack=True,
        )

    @property
    def id(self) -> str:
        """Return RPC client id

        Returns:
            str: rpc client id
        """
        return self.__id

    def __on_response(
        self,
        ch: BlockingChannel,
        method: Basic.Deliver,
        props: BasicProperties,
        body: bytes,
    ):
        """Callback triggered on response to a message published into {self.request_queue}.
        The response is published into a private queue between this RPC client and the server.

        Args:
            ch (BlockingChannel): _description_
            method (Basic.Deliver): _description_
            props (BasicProperties): _description_
            body (bytes): _description_
        """
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def send_request(self, request: str) -> dict:
        """Send JSON request to {self.request_queue}.
        It will wait the reply from the server host,
        which is the output of the VBoxManage command.

        Args:
            request (dict): api_vbox request to execute on server host

        Returns:
            dict: reply from server host
        """
        self.response = None
        self.corr_id = str(uuid.uuid4())  # request unique id
        request_body = dict(client_id=self.__id, req=request)
        # STEP 2: publish message within the queue
        self.__channel.basic_publish(
            exchange="",
            routing_key=self.request_queue,  # QUEUE to publish
            properties=pika.BasicProperties(
                reply_to=self.reply_queue,  # private QUEUE that will be used to reply
                correlation_id=self.corr_id,
                content_type="application/json",
                content_encoding="utf-8",
            ),
            body=json.dumps(request_body),
        )
        self.__connection.process_data_events(
            time_limit=self.REPLY_WAITING_SECONDS_LIMIT
        )
        return self.response
