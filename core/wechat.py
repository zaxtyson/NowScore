import requests
from typing import List
from utils.logger import logger


class WechatPusher:

    def __init__(self):
        self._send_keys = []

    def set_sed_keys(self, send_keys: List[str]):
        self._send_keys = send_keys

    @staticmethod
    def _push_one(title: str, msg: str, key: str) -> bool:
        url = f"https://sc.ftqq.com/{key}.send"
        payload = {
            "text": title,
            "desp": msg
        }
        resp = requests.post(url, data=payload)
        if resp.status_code != 200:
            logger.error(f"Send msg [{title}] => {key} failed!")
            return False
        logger.info(f"Send msg [{title}] => {key} success!")
        return True

    def push(self, title: str, msg: str):
        for key in self._send_keys:
            for _ in range(3):
                if self._push_one(title, msg, key):
                    break
                # send failed, try again
