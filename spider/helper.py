from time import sleep
from typing import Optional

from aiohttp import ClientSession, ClientResponse, ClientTimeout
from lxml import etree

from spider.proxy import ProxyPool
from spider.user_agent import get_random_ua
from utils.logger import logger

__all__ = ["HtmlParseHelper"]


class HtmlParseHelper:

    def __init__(self):
        self._use_proxy_pool = True
        self._proxy_pool = ProxyPool()
        self._session = ClientSession()

    def wait_proxy_available(self):
        if not self._use_proxy_pool:
            logger.info("ProxyPool is not enable")
            return

        self._proxy_pool.setDaemon(True)
        self._proxy_pool.start()
        while not self._proxy_pool.has_available_proxy():
            logger.info("Waiting for proxy available...")
            sleep(1)

    def enable_proxy_pool(self, use: bool):
        self._use_proxy_pool = use

    async def close_session(self):
        if self._session:
            await self._session.close()
        self._proxy_pool.stop()

    def _set_headers(self, kwargs: dict):
        """Set headers, if not set "User-Agent", use random ua"""
        kwargs.setdefault("timeout", ClientTimeout(total=30, sock_connect=15))
        if self._use_proxy_pool:
            kwargs.setdefault("proxy", self._proxy_pool.get_random_proxy())

        if "headers" not in kwargs:
            kwargs["headers"] = {"User-Agent": get_random_ua()}
        else:
            keys = [key.lower() for key in kwargs.get("headers")]
            if "user-agent" not in keys:  # headers set, but not User-Agent
                kwargs["headers"]["user-agent"] = get_random_ua()

    async def get(self, url: str, params: dict = None, **kwargs) -> Optional[ClientResponse]:
        for _ in range(3):
            try:
                self._set_headers(kwargs)
                logger.debug(f"GET {url} | Params: {params} | Args: {kwargs}")
                resp = await self._session.get(url, params=params, **kwargs)
                logger.debug(f"Code: {resp.status} | Type: {resp.content_type} | Length: {resp.content_length} ({url})")
                return resp
            except Exception as e:
                if self._use_proxy_pool:
                    self._proxy_pool.remove_proxy(kwargs["proxy"])
                logger.warning(f"Exception in {self.__class__}: {e}")

    async def post(self, url: str, data: dict = None, **kwargs) -> Optional[ClientResponse]:
        for _ in range(3):
            try:
                self._set_headers(kwargs)
                logger.debug(f"POST {url} | Data: {data} | Args: {kwargs}")
                resp = await self._session.post(url, data=data, **kwargs)
                logger.debug(f"Code: {resp.status} | Type: {resp.content_type} | Length: {resp.content_length} ({url})")
                return resp
            except Exception as e:
                if self._use_proxy_pool:
                    self._proxy_pool.remove_proxy(kwargs["proxy"])
                logger.warning(f"Exception in {self.__class__}: {e}")

    async def get_text(self, url: str, expect_code: int = 200) -> str:
        for _ in range(2):
            try:
                resp = await self.get(url)
                if not resp or resp.status != expect_code:
                    return ""
                return await resp.text()
            except Exception as e:  # maybe timeout here
                logger.error(f"Failed to get {url}, {e}")
        return ""

    @staticmethod
    def xpath(html: str, xpath: str) -> Optional[etree.Element]:
        if not html:
            return None
        try:
            return etree.HTML(html).xpath(xpath)
        except Exception as e:
            logger.exception(e)
            return None
