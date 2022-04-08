"""
System commands useful for the api.

@author Rxinui
"""
import os
import subprocess
from threading import ThreadError, Timer
from typing import List, Any, Optional, Tuple, Union
from rabbitmq.rpc import RPCClient
from .logmodule import logger

EXECMODE_CONTAINER = "container"
EXECMODE_LOCAL = "local"
CONTAINER_EXEC_TIMEOUT = 300  # in seconds
LOCAL_EXEC_TIMEOUT = 300  # in seconds
EXIT_TIMEOUT_EXPIRED = -1000

logger = logger(__name__, "main.py.log")


def execute_cmd(
    user: Any, cmd: List[str], execmode: Optional[str] = None
) -> Tuple[str, str, int]:
    """Execute a shell command.

    Args:
        user (Any): user id
        cmd (List[str]): command
        execmode (Optional[str]): execution mode 'local' or 'container'

    Raises:
        EnvironmentError: undefined API_VBOX_EXECMODE env

    Returns:
        Tuple[str,str,int]: command output, error and returncode
    """
    if not execmode:
        execmode = os.getenv("API_VBOX_EXECMODE")
    if execmode == EXECMODE_CONTAINER:
        with RPCClient(user, os.getenv("API_VBOX_USERS_REQUEST_QUEUE")) as rpc:
            response = rpc.send_request({"cmd": cmd})
            output, error, exit_code = (
                response["res"]["output"],
                response["res"]["error"],
                response["res"]["exit_code"],
            )
    elif execmode == EXECMODE_LOCAL:
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
    if exit_code == 0:
        logger.info("Command %s has been successfully executed", cmd)
    else:
        logger.error("Command %s has been failed (exit=%s)", cmd, exit_code)
        logger.error("Command error details: %s", error)
    return output, error, exit_code


def execute_future_cmd(
    user: Any,
    cmd: List[str],
    seconds: Union[int, float],
    execmode: Optional[str] = EXECMODE_LOCAL,
):
    """Execute a shell command in the future using Thread.Timer.

    Args:
        user (Any): user id
        cmd (List[str]): command
        seconds (Union[int, float]): interval in seconds before executing command
        execmode (Optional[str], optional): execution mode of the future command.
                                            Defaults to EXECMODE_LOCAL.
    """
    try:
        t = Timer(seconds, execute_cmd, [user, cmd, execmode])
        t.setName(f"timer.user.{user}")
        t.start()
        logger.info(
            "Future command %s has been launched on a Timer %s", cmd, t.getName()
        )
    except ThreadError as thread_exc:
        logger.error(thread_exc)
    except SystemError as system_exc:
        logger.error(system_exc)
        t.cancel()
        logger.warning("Thread has been cancel manually.")
