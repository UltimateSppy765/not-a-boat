import logging

from discord import utils

log_handler = logging.StreamHandler()

if utils.stream_supports_colour(log_handler.stream):
    default_log_formatter = utils._ColourFormatter()
else:
    default_log_formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )


def setuplogger(
    module_name: str,
    log_level: int | None = logging.INFO,
    log_formatter: logging.Formatter | None = default_log_formatter,
) -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    return logger
