import logging
from .config import Config
import time

class Logger:
    def __init__(self, name: str) -> None:
        formatter = logging.Formatter(
            Config.get("LOG_FORMAT"),
            Config.get("LOG_DATE_FORMAT")
        )

        self.name = name
        self.file_handler = logging.FileHandler(
            time.strftime(Config.get("LOG_PATH"), time.localtime())
        )
        self.file_handler.setFormatter(formatter)

    def __log(self, level: int, message: str) -> None:
        logger = logging.getLogger(self.name)
        logger.addHandler(self.file_handler)
        logger.setLevel(level)

        logger.log(level, message)

    def debug(self, message: str) -> None:
        if Config.get("ENVIRONMENT") == "production":
            return
        
        self.__log(logging.DEBUG, message)

    def info(self, message: str) -> None:
        self.__log(logging.INFO, message)

    def warning(self, message: str) -> None:
        self.__log(logging.WARNING, message)

    def error(self, message: str) -> None:
        self.__log(logging.ERROR, message)

    def critical(self, message: str) -> None:
        self.__log(logging.CRITICAL, message)