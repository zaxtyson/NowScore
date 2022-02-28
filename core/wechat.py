from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from typing import List
from utils.logger import logger
import time


class WechatPusher:

    def __init__(self):
        self._send_keys = []
        self._executor = ThreadPoolExecutor(max_workers=3)

    def set_sed_keys(self, send_keys: List[str]):
        self._send_keys = send_keys

    @staticmethod
    def _push_one(title: str, msg: str, key: str) -> bool:
        url = f"https://sc.ftqq.com/{key}.send"
        payload = {
            "text": title,
            "desp": msg
        }
        try:
            resp = requests.post(url, data=payload)
            if resp.status_code != 200:
                logger.error(f"Send msg [{title}] => {key} failed!")
                return False
            logger.info(f"Send msg [{title}] => {key} success!")
            return True
        except Exception as e:  # timeout, SSLError...
            logger.warn(f"Send msg [{title}] failed: {e}")
            return False

    @staticmethod
    def _push_one_insurance(title: str, msg: str, key: str) -> None:
        for _ in range(3):
            if WechatPusher._push_one(title, msg, key):
                break
            # send failed, try again

    def _push_repeat(self, title: str, msg: str, key: str, repeat: int, interval: float):
        for i in range(repeat):
            self._push_one_insurance(title, msg, key)
            time.sleep(interval)  # user demand...

    def push(self, title: str, msg: str, *, repeat: int, interval: float):
        tasks = [self._executor.submit(self._push_repeat, title, msg, key, repeat, interval)
                 for key in self._send_keys]
        # wait for task finished
        for task in as_completed(tasks):
            task.result()
