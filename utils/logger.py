import logging
import os
from logging.handlers import TimedRotatingFileHandler

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

# Output log to file(only save the nearest 3 hours)
logging_path = os.path.dirname(__file__) + "/../logs"
if not os.path.exists(logging_path):
    os.makedirs(logging_path)
file_handler = TimedRotatingFileHandler(
    filename=logging_path + "/app.log",
    when="H",
    interval=1,
    backupCount=3,
    encoding="utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
