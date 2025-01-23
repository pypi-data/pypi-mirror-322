"""
The LogManager class provides loggers that share file and stream handlers.
"""

import logging
from logging.handlers import RotatingFileHandler


class LogManager:
    """
    The LogManager class provides loggers that share file and stream handlers.
    """

    log_filename = "quiz_wiz.log"
    log_file_size = 2097152
    log_file_backup = 10
    file_formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)5.5s %(name)20.20s %(lineno)5d - %(message)s"
    )
    file_handler = RotatingFileHandler(
        filename=log_filename, maxBytes=log_file_size, backupCount=log_file_backup
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    stream_formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)5.5s %(name)20.20s - %(message)s"
    )
    stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(logging.INFO)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(stream_formatter)
    logger_map: dict[str, str] = {}

    @classmethod
    def get_logger(cls, name):
        """
        get_logger return stream/file handler
        """
        logger = logging.getLogger(name)
        if name in cls.logger_map:
            return logger

        logger.addHandler(cls.stream_handler)
        logger.addHandler(cls.file_handler)
        logger.setLevel(logging.DEBUG)
        cls.logger_map[name] = logger
        return logger

    @classmethod
    def set_stream_level(cls, level):
        """
        set_stream_level set level
        """
        cls.stream_handler.setLevel(level)

    @classmethod
    def change_log_file(cls, log_file="quiz_wiz.log"):
        """
        if log_file exceeds the maxBytes, change the log file
        """
        if log_file == cls.log_filename:
            return

        new_file_handler = RotatingFileHandler(
            filename=log_file, maxBytes=1000000, backupCount=10
        )
        new_file_handler.setLevel(logging.DEBUG)
        new_file_handler.setFormatter(cls.file_formatter)

        for logger in cls.logger_map.values():
            logger.removeHandler(cls.file_handler)
            logger.addHandler(new_file_handler)

        cls.log_filename = log_file
        cls.file_handler = new_file_handler
