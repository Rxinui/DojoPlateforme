"""
Global Python3 logger object configured for this project.

@author Rxinui
@date 2022-01-31
"""
import logging
from typing import Literal

formatter = logging.Formatter(
    "%(asctime)s::%(name)s::%(levelname)s::%(message)s", datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_logger(name: str, logfile: str, level: Literal) -> logging.Logger:
    """
    Create a logger {name} for a given {logfile} that follows the global configuration.

    Args:
        name (str): logger name
        logfile (str): log output file
        level (Literal): log level

    Returns:
        logging.Logger: new logger
    """
    handler = logging.FileHandler(logfile, encoding="utf-8")
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
