import logging


def get_logger(log_level: int = logging.INFO) -> logging.Logger:
    if "logger" in globals():
        return globals()["logger"]
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(
        logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S %z")
    )
    logger.addHandler(stream_handler)
    return logger


logger = get_logger()
