import asyncio
import queue
import re
from typing import Callable, List

from lxml.etree import Element
import datetime
from core.helper import HtmlParseHelper
from core.model import LeagueMetaInfo, LeagueDetailInfo
from utils.logger import logger


class NowScoreSpider(HtmlParseHelper):

    def __init__(self):
        super().__init__()
        self._meta_filter = None
        self._detail_filter = None
        self._meta_callback = None
        self._meta_queue = queue.Queue()

    def set_meta_filter(self, pred: Callable[[LeagueMetaInfo], bool]):
        self._meta_filter = pred

    def set_detail_filter(self, pred: Callable[[LeagueDetailInfo], bool]):
        self._detail_filter = pred

    def set_meta_callback(self, callback: Callable[[LeagueMetaInfo], None]):
        """The callback will be called when we got a useful meta
        info immediately, thus this callback should NOT cost
        too much time in processing meta info, or it will block
        the main event loop
        """
        self._meta_callback = callback

    def get_meta_queue(self):
        """Processing meta info in other threads to avoid blocking
        main event loop"""
        return self._meta_queue

    def get_meta_list(self) -> List[LeagueMetaInfo]:
        """Consume all data in meta_queue, return meta list"""
        meta_list = []
        while not self._meta_queue.empty():
            meta_list.append(self._meta_queue.get())
        return meta_list

    async def _parse_meta_info(self, date: str):
        url = f"http://live.nowscore.com/1x2/bet007history.htm?matchdate={date}"
        resp = await self.get(url)
        if not resp or resp.status != 200:
            return
        html = await resp.text()
        # parse info from html
        data = self.xpath(html, "//tr[@name]")
        for item in data:
            yield self._extract_meta_info(item)

    async def _parse_detail_info(self, meta: LeagueMetaInfo):
        detail = LeagueDetailInfo()
        detail.meta = meta

        # Parse match state info
        # See: http://score.nowscore.com/script/football/LiveMatchState.js
        # schedule_id = self.xpath(html, '//input[@id="hide_scheduleId"]/@value')[0]
        schedule_id = meta.detail_url.replace(".htm", "")  # ID can be found in url

        # in function scoreobj(data)
        url = "http://live.nowscore.com/football/GetLiveScore?scheid=" + schedule_id
        resp = await self.get(url)
        if not resp or resp.status != 200:
            return detail  # error
        data = await resp.text()
        q = data.split("^")
        detail.state = int(q[4])

        # Parse other info
        url = f"http://1x2.nowscore.com/{schedule_id}.js"
        resp = await self.get(url)
        if not resp or resp.status != 200:
            return detail  # error
        data = await resp.text()
        game = re.search(r"var game=Array\((.+)\);", data)
        # `eval` may be dangerous, but it really convenience :)
        # game = ['xxx|xxx|xxx', 'xxx|xxx|xxx']
        game = eval(f"[{game.group(1)}]")
        # game_detail = re.search(r"var game=gameDetail\((.+)\);", data)
        # game_detail = eval(f"[{game_detail.group(1)}]")

        # Get Bet365 host_win field
        # See: http://score.nowscore.com/1x2/1x2.js
        # in function CreateTable()
        for item in game:
            if "Bet 365" in item:
                # index 3 is 即时, index 10 is 初指
                detail.bet365_host_win = float(item.split("|")[10])

        # Calculate kali index
        index1 = []
        index2 = []
        index3 = []
        for item in game:
            item = item.split("|")
            index1.append(float(item[17]))
            index2.append(float(item[18]))
            index3.append(float(item[19]))
        detail.index_low = [min(index1), min(index2), min(index3)]
        detail.index_high = [max(index1), max(index2), max(index3)]
        detail.index_avg = [sum(index1) / len(index1), sum(index2) / len(index2), sum(index3) / len(index3)]
        return detail

    @staticmethod
    def _extract_meta_info(item: Element):
        info = LeagueMetaInfo()
        info.name = item.xpath("td[1]/text()")[0]
        info.time = item.xpath("td[2]/text()")[0]
        home_team = item.xpath('td[@class="team"][1]/a//text()')
        info.home_team = "".join(home_team).strip()
        guest_team = item.xpath('td[@class="team"][2]/a//text()')
        info.guest_team = "".join(guest_team).strip()
        info.score = item.xpath('.//font[@color="red"]/text()')[0]
        company_num = item.xpath('td[@class="gocheck"]/text()')[0]
        info.company_num = int(company_num.strip("()"))
        info.detail_url = item.xpath('td[@class="gocheck"]/a/@href')[0]  # "2137086.htm"
        return info

    def _is_meta_useful(self, meta: LeagueMetaInfo) -> bool:
        if self._meta_filter:  # if user set meta filter
            if not self._meta_filter(meta):  # drop this meta info
                logger.warn(f"Drop meta data {meta}")
                return False
        # no set filter or this info is useful
        return True

    def _is_detail_useful(self, detail: LeagueDetailInfo) -> bool:
        if self._detail_filter:
            if not self._detail_filter(detail):
                logger.warn(f"Drop detail data {detail}")
                return False
        # no set filter or this info is useful
        return True

    async def _parse_one_page(self, date: str):
        logger.info(f"Parse page on {date}")
        async for meta in self._parse_meta_info(date):
            if not self._is_meta_useful(meta):
                continue  # drop this meta info
            detail = await self._parse_detail_info(meta)
            if not self._is_detail_useful(detail):
                continue
            # this is what we need
            self._meta_queue.put(meta)
            if self._meta_callback:
                self._meta_callback(meta)

    async def _main(self):
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        await self._parse_one_page(yesterday.strftime("%Y-%m-%d"))
        await self._parse_one_page(today.strftime("%Y-%m-%d"))
        await self.close_session()

    def run(self):
        logger.info("\n\n" + "=" * 100)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._main())
