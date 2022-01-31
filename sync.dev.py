"""
@author Rxinui
@date 2022-01-25
@updated 2022-01-26

Synchronise the following project with remote server host
which operates as production environnement.
It aims to work on a production-like environnement locally.

Purpose:
    Clone this production environnement on local host to work locally
    without damaging the production.

What it does:
    Synchronise the whole production environnement that it is ignored by git.
    For instance, VMs files are too heavy to be commited with git.
    Therefore, this script retrieves project files and updates locally
    from remote server in order will allow the developpers to work locally
    with a production-like environnement.

Important:
    The synchronisation is unidirectional from remote server host to local host.
    Hence, it is necessary to possess a SSH access by public key to the remote server.
"""

import json
import re
import subprocess as subp
import sys
from pathlib import Path
from functools import reduce
from typing import Tuple, Union, List
from datetime import datetime
import paramiko
from libraries.python3 import get_logger, INFO

LocalCommandError = subp.CalledProcessError
RemoteCommandError = paramiko.ChannelException

EXIT_OK = 0
EXIT_REMOTE_COMMAND_ERROR = -31000
EXIT_LOCAL_COMMAND_ERROR = -31001
EXIT_NO_REMOTE_SYNC_CONF = -31002

logger = get_logger(__file__, f"{__file__}.log", level=INFO)
sync_server_conf = {}
sync_client_conf = {}

with open("./.sync.client.json", encoding="utf-8") as fp:
    sync_client_conf = json.load(fp)


def ssh_connect() -> paramiko.SSHClient:
    """Enable SSH client connexion.

    Returns:
        paramiko.SSHClient: ssh client
    """
    clientconf = sync_client_conf["client"]
    ssh_config = paramiko.SSHConfig.from_path(clientconf["sshConfPath"])
    ssh_config = ssh_config.lookup(clientconf["sshHost"])
    _ssh_client = paramiko.SSHClient()
    _ssh_client.load_system_host_keys()
    password = (
        {
            "key_filename": clientconf["sshPrivateKeyPath"],
            "password": input("SSH Passphrase: "),
        }
        if "sshPrivateKeyPath" in clientconf
        else {"password": input("SSH Password: ")}
    )
    _ssh_client.connect(
        hostname=ssh_config["hostname"], username=ssh_config["user"], **password
    )
    logger.info(
        "SSH connection '%s@%s' is established",
        ssh_config["user"],
        ssh_config["hostname"],
    )
    return _ssh_client


def exec_remote_command(command: str) -> Tuple[str, str]:
    """Execute a command on remote host.

    Args:
        command (str): command to execute

    Returns:
        Tuple[str,str]: stdout of command, stderr of command
    """
    _, stdout, stderr = ssh_client.exec_command(command)
    _.close()
    return stdout.read().decode("utf-8"), stderr.read().decode("utf-8")


def exec_local_command(command: str) -> str:
    """Execute a command on local host.

    Args:
        command (str): command to execute

    Returns:
        str: output of command
    """
    return subp.check_output(command.split(), stderr=subp.DEVNULL).decode("utf-8")


def _load_sync_config(out: dict, conf: Path):
    """Load synchronisation config file from remote host.

    Args:
        out (dict): conf dict object
        conf (Path, optional): path to config file on remote host. Defaults to PATH_CONF_SYNC.
    """
    output, _ = exec_remote_command(f"cat {conf}")
    out.update(json.loads(output))
    return logger.info("Synchronisation configuration '%s' is loaded.", conf)


def list_necessary_dir() -> List[str]:
    """
    List directories that are considered as necessary for prod environment.

    Returns:
        List[str]: list of directories path
    """
    if not sync_server_conf:
        logger.error("Unable to load synchronisation config on remote server.")
        sys.exit(EXIT_NO_REMOTE_SYNC_CONF)
    cmd_list_directories = f'find {sync_server_conf["server"]["projectPath"]} -type f'
    if sync_server_conf["server"]["ignore"]:
        logger.info("Ignoring %s.", sync_server_conf["server"]["ignore"])
        cmd_list_directories = reduce(
            lambda acc, s: acc + f" -not -path *{s}",
            sync_server_conf["server"]["ignore"],
            cmd_list_directories,
        )
    output = exec_remote_command(cmd_list_directories)[0]
    logger.info("Command ran: %s", cmd_list_directories)
    return sorted(output.split(), key=len, reverse=True)


def _file_has_changes(filename: Union[Path, str]) -> bool:
    """Check if the given filename has been updated on remote host.

    Args:
        filename (Union[Path,str]): remote filename

    Returns:
        bool: True if updated else False
    """

    def extract_datetime_filename(out: str) -> datetime:
        return datetime.fromisoformat(
            re.search(r".*(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})\s[\w\W\d]+$", out).group(1)
        )

    def build_ls(path: Path) -> str:
        return f"ls -lhA --time-style=long-iso {Path(path)}"

    has_file_locally = True
    relative_filename = Path(
        Path(filename).relative_to(sync_server_conf["server"]["projectPath"])
    )
    try:
        remote_output, _ = exec_remote_command(build_ls(filename))
        remote_datetime = extract_datetime_filename(remote_output)
        local_datetime = datetime.fromtimestamp(relative_filename.stat().st_mtime)
        deltatime = remote_datetime - local_datetime
    except RemoteCommandError:
        sys.exit(EXIT_REMOTE_COMMAND_ERROR)
    except (LocalCommandError, FileNotFoundError):
        has_file_locally = False
    return not has_file_locally or deltatime.total_seconds() > 0


def pull_file_locally(sftp: paramiko.SFTPClient, filename: Union[Path, str]):
    """Download a file from remote host to local host.

    It occurs if the given file is only present on remote host
    or if remote file has been updated compared to the local file.

    Args:
        sftp (paramiko.SFTPClient): sftp client
        filename (Union[Path,str]): file
    """

    def log_transfer(size_sent, size_remaining):
        print(
            f"SFTP GET '{filename}' {round(size_sent / size_remaining * 100,1)}%",
            end="\r",
        )
        if size_sent == size_remaining:
            print("\n")

    if not _file_has_changes(filename):
        return logger.info("'%s' does not have any new changes.", filename)
    logger.info("'%s' has new changes.", filename)
    relative_filename = Path(
        Path(filename).relative_to(sync_server_conf["server"]["projectPath"])
    )
    relative_filename.parent.mkdir(parents=True, exist_ok=True)
    logger.info("'%s' directory is created.", relative_filename.parent)
    logger.info("'%s' SFTP GET is starting.", relative_filename)
    sftp.get(remotepath=filename, localpath=relative_filename, callback=log_transfer)
    return logger.info("'%s' SFTP GET is now updated on local host.", relative_filename)


if __name__ == "__main__":
    logger.info("Synchronisation...")
    ssh_client = ssh_connect()
    sftp_client = ssh_client.open_sftp()
    _load_sync_config(sync_server_conf, conf=sync_client_conf["server"]["syncConfPath"])
    logger.info(sync_server_conf)
    directories = list_necessary_dir()
    for remote_filename in directories:
        pull_file_locally(sftp_client, remote_filename)
    logger.info("End of synchronisation.")
    sys.exit(EXIT_OK)
