"""
System commands useful for the api.

@author Rxinui
"""
import os
import subprocess
from typing import List, Any, Tuple
from rabbitmq.rpc import RPCClient

EXECMODE_CONTAINER = "container"
EXECMODE_LOCAL = "local"
CONTAINER_EXEC_TIMEOUT = 300  # in seconds
LOCAL_EXEC_TIMEOUT = 300  # in seconds
EXIT_TIMEOUT_EXPIRED = -1000


def execute_cmd(user: Any, cmd: List[str]) -> Tuple[str, str, int]:
    """Execute a shell command.

    Args:
        cmd (List[str]): command

    Returns:
        str: command output
    """
    if os.environ["API_VBOX_EXECMODE"] == EXECMODE_CONTAINER:
        with RPCClient(user, os.getenv("API_VBOX_USERS_REQUEST_QUEUE")) as rpc:
            response = rpc.send_request({"cmd": cmd})
            output, error, exit_code = (
                response["res"]["output"],
                response["res"]["error"],
                response["res"]["exit_code"],
            )
    elif os.environ["API_VBOX_EXECMODE"] == EXECMODE_LOCAL:
        with subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) as proc:
            try:
                output, error = proc.communicate(timeout=LOCAL_EXEC_TIMEOUT)
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
    else:
        raise EnvironmentError("API_VBOX_EXECMODE env variable is missing.")
    return output, error, exit_code
