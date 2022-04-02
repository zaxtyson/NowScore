import json
from datetime import datetime
from os.path import dirname

from db.model import MetaItem
from utils.logger import logger


class ParseHistory:

    def __init__(self):
        self._parsed_urls = set()
        self._file = dirname(__file__) + "/history.json"

    def load(self):
        with open(self._file, "r") as f:
            info = json.load(f)
            """
            {
                "date_utc": "2022-03-31",
                "url": [
                    "xxxx.htm"
                ]
            }
            """
            history = datetime.strptime(info["date_utc"], "%Y-%m-%d")
            # if history is today, load urls, otherwise, drop urls
            if history.date() == datetime.utcnow().date():
                self._parsed_urls = set(info["url"])
            logger.info(f"Load parsed urls: {len(self._parsed_urls)}")

    def add(self, meta: MetaItem):
        self._parsed_urls.add(meta.detail_url)

    def contains(self, meta: MetaItem):
        return meta.detail_url in self._parsed_urls

    def save(self):
        now_utc = datetime.utcnow().strftime("%Y-%m-%d")
        info = {"date_utc": now_utc, "url": list(self._parsed_urls)}
        with open(self._file, "w") as f:
            logger.info(f"Update parsed urls: {len(self._parsed_urls)}")
            json.dump(info, f, indent=4)
