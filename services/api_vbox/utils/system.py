"""
System commands useful for the api.

@author Rxinui
"""
import os
import subprocess
from typing import List, Any
from rabbitmq.rpc import RPCClient

EXECMODE_CONTAINER = "container"
EXECMODE_LOCAL = "local"


def execute_cmd(user: Any, cmd: List[str]) -> str:
    """Execute a shell command.

    Args:
        cmd (List[str]): command

    Returns:
        str: command output
    """
    if os.environ["API_VBOX_EXECMODE"] == EXECMODE_CONTAINER:
        with RPCClient(user, os.getenv("API_VBOX_USERS_REQUEST_QUEUE")) as rpc:
            response = rpc.send_request({"cmd": cmd})
            output = response["res"]["output"]
    elif os.environ["API_VBOX_EXECMODE"] == EXECMODE_LOCAL:
        with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
            output = proc.communicate()[0].decode("utf-8")
    else:
        raise EnvironmentError("API_VBOX_EXECMODE env variable is missing.")
    return output
