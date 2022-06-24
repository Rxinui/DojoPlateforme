"""
Global Python3 logger object configured for this project.

@author Rxinui
@date 2022-01-31
"""
import os
import logging

formatter = logging.Formatter(
    "%(asctime)s::%(name)s::%(levelname)s::%(message)s", datefmt="%Y-%m-%dT%H:%M:%S"
)

def logger(name: str, logfile: str) -> logging.Logger:
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
    # stream_handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    # stream_handler.setFormatter(formatter)
    _logger = logging.getLogger(name)
    if not os.getenv("APP_ENVIRONMENT") or os.getenv(
        "APP_ENVIRONMENT"
    ).lower().startswith("dev"):
        _logger.setLevel(logging.DEBUG)
    elif os.getenv("APP_ENVIRONMENT").lower().startswith("prod"):
        _logger.setLevel(logging.INFO)
    _logger.addHandler(handler)
    # _logger.addHandler(stream_handler)
    return _logger
