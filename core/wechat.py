import requests

from utils.logger import logger


class WechatPusher:

    def __init__(self):
        self._send_key = ""

    def set_sed_key(self, send_key: str):
        self._send_key = send_key

    def push(self, title: str, msg: str):
        url = f"https://sc.ftqq.com/{self._send_key}.send"
        payload = {
            "text": title,
            "desp": msg
        }
        resp = requests.post(url, data=payload)
        if resp.status_code != 200:
            logger.error(f"Send msg [{title}] failed!")
            return
        logger.info(f"Send msg [{title}] success!")
