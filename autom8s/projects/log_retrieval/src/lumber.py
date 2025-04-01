"""What comes from logging? LUMBER"""

import logging


def set_log_level(level: int = logging.INFO) -> None:
    """Set the log level for the application (at start of application)

    It is recommended to only call this function once at the beginning of the
    application.

    Args:
        level (logging.Level): The log level to set.
    """
    logging.basicConfig(level=level)
