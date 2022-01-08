from typing import Optional

from aiohttp import ClientSession, ClientResponse, ClientTimeout
from lxml import etree

from utils.logger import logger
from utils.user_agent import get_random_ua

__all__ = ["HtmlParseHelper"]


class HtmlParseHelper:

    def __init__(self):
        self._session = ClientSession()

    async def close_session(self):
        if self._session:
            await self._session.close()

    @staticmethod
    def _set_headers(kwargs: dict):
        """Set headers, if not set "User-Agent", use random ua"""
        kwargs.setdefault("timeout", ClientTimeout(total=30, sock_connect=5))

        if "headers" not in kwargs:
            kwargs["headers"] = {"User-Agent": get_random_ua()}
        else:
            keys = [key.lower() for key in kwargs.get("headers")]
            if "user-agent" not in keys:  # headers set, but not User-Agent
                kwargs["headers"]["user-agent"] = get_random_ua()

    async def get(self, url: str, params: dict = None, **kwargs) -> Optional[ClientResponse]:
        try:
            self._set_headers(kwargs)
            logger.debug(f"GET {url} | Params: {params} | Args: {kwargs}")
            resp = await self._session.get(url, params=params, **kwargs)
            logger.debug(f"Code: {resp.status} | Type: {resp.content_type} | Length: {resp.content_length} ({url})")
            return resp
        except Exception as e:
            logger.warning(f"Exception in {self.__class__}: {e}")

    async def post(self, url: str, data: dict = None, **kwargs) -> Optional[ClientResponse]:
        try:
            self._set_headers(kwargs)
            logger.debug(f"POST {url} | Data: {data} | Args: {kwargs}")
            resp = await self._session.post(url, data=data, **kwargs)
            logger.debug(f"Code: {resp.status} | Type: {resp.content_type} | Length: {resp.content_length} ({url})")
            return resp
        except Exception as e:
            logger.warning(f"Exception in {self.__class__}: {e}")

    @staticmethod
    def xpath(html: str, xpath: str) -> Optional[etree.Element]:
        if not html:
            return None
        try:
            return etree.HTML(html).xpath(xpath)
        except Exception as e:
            logger.exception(e)
            return None
