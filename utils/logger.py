import logging
import os
from logging.handlers import RotatingFileHandler

__all__ = ["logger"]

# Logger Config
logger = logging.getLogger('now_score')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    fmt="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Output log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Output log to file
logging_path = os.path.dirname(__file__) + "/../logs"
if not os.path.exists(logging_path):
    os.makedirs(logging_path)
file_handler = RotatingFileHandler(
    filename=logging_path + "/app.log",
    mode="a",
    maxBytes=10 * 1024 * 1024,
    backupCount=50,
    encoding="utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
