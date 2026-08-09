import logging
from pathlib import Path

from ..config import settings

log_directory = Path(settings.LOG_DIRECTORY)
log_directory.mkdir(parents=True, exist_ok=True)

log_file_path = log_directory / settings.LOG_FILE_NAME

def configure_logger() -> None:
    logging.basicConfig(
        level =  settings.LOG_LEVEL.upper(),
        format = "%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        handlers = [
            logging.FileHandler(log_file_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)