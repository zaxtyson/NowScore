import queue
import re
from datetime import datetime
from typing import List

from lxml.etree import Element

from db.model import MetaItem, DetailInfo, DetailItem, TrendingItem
from db.session import SqlSession
from spider.helper import HtmlParseHelper
from spider.history import ParseHistory
from strategy.base import BaseStrategy
from utils.logger import logger


class NowScoreSpider(HtmlParseHelper):

    def __init__(self):
        super().__init__()
        self._this_year = "2022"
        self._enable_proxy_pool = False
        self._close_session_after_parse = False

        self._meta_queue = queue.Queue()
        self._strategy = BaseStrategy()
        self._db = SqlSession()
        self._history = ParseHistory()

    def settings(self, *,
                 strategy: BaseStrategy,
                 persistence_history: bool = False,
                 enable_proxy_pool: bool = False,
                 close_session_after_done: bool = True):
        self._history.persistence_to_file(persistence_history)
        self.enable_proxy_pool(enable_proxy_pool)
        self._strategy = strategy
        self._close_session_after_parse = close_session_after_done

    def get_meta_list(self) -> List[MetaItem]:
        """Consume all data in meta_queue, return meta list"""
        meta_list = []
        while not self._meta_queue.empty():
            meta_list.append(self._meta_queue.get())
        return meta_list

    async def _parse_meta_item(self, date: str):
        url = f"http://live.nowscore.com/1x2/bet007history.htm?matchdate={date}"
        logger.info(f"Parse page: {url}")
        html = await self.get_text(url)
        # parse info from html
        data = self.xpath(html, "//tr[@name]")
        for item in data:
            yield self._extract_meta_item(item)

    async def _parse_detail_info(self, meta: MetaItem) -> DetailInfo:
        detail = DetailInfo()
        detail.meta = meta

        # Parse match state info
        # See: http://score.nowscore.com/script/football/LiveMatchState.js
        # schedule_id = self.xpath(html, '//input[@id="hide_scheduleId"]/@value')[0]
        schedule_id = meta.detail_url.replace(".htm", "")  # ID can be found in url
        logger.info(f"Parse detail page: http://live.nowscore.com/1x2/{meta.detail_url}")

        # in function scoreobj(data)
        url = "http://live.nowscore.com/football/GetLiveScore?scheid=" + schedule_id
        data = await self.get_text(url)
        if not data:
            return detail  # error
        q = data.split("^")
        detail.state = int(q[4])

        # Parse other info
        url = f"http://1x2.nowscore.com/{schedule_id}.js"
        data = await self.get_text(url)
        if not data:
            return detail  # error

        game = re.search(r"var game=Array\((.+)\);", data)
        # `eval` may be dangerous, but it really convenience :)
        # game = ['xxx|xxx|xxx', 'xxx|xxx|xxx']
        game = eval(f"[{game.group(1)}]")
        game_detail = re.search(r"var gameDetail=Array\((.+)\);", data)
        game_detail = eval(f"[{game_detail.group(1)}]")

        # Get Bet365 host_win field
        # See: http://score.nowscore.com/1x2/1x2.js
        # in function CreateTable()
        # "281|110510197|Bet 365|4|3.8|1.67|22.48|23.67|53.85|89.93|5.25|4|1.5|17.2|
        # 22.58|60.22|90.32|0.91|0.93|0.89|2022,03-1,31,00,00,00|365(英国)|1|0"

        for item_str in game:
            item = item_str.split("|")
            item_id = item[1]  # '110509523'
            detail.items.append(DetailItem(
                item_id=int(item_id),
                detail_url=meta.detail_url,
                company_name_en=item[2],
                company_name_zh=item[21],
                initial_host_win=round(float(item[3]), 2),
                initial_draw=round(float(item[4]), 2),
                initial_guest_win=round(float(item[5]), 2),
                initial_return_rate=round(float(item[9]), 2),
                instant_host_win=round(float(item[10]), 2),
                instant_draw=round(float(item[11]), 2),
                instant_guest_win=round(float(item[12]), 2),
                instant_return_rate=round(float(item[16]), 2),
                kali_low=round(float(item[17]), 2),
                kali_mid=round(float(item[18]), 2),
                kali_high=round(float(item[19]), 2),
                is_main_company=bool(int(item[22])),
                is_exchange=bool(int(item[23])),
                trending_list=self._get_trending_list(game_detail, item_id),
            ))

        return detail

    def _get_trending_list(self, all_trending_list: List[str], item_id: str) -> List[TrendingItem]:
        ret = []
        company_trending = ""
        for trending_list in all_trending_list:
            if trending_list.startswith(item_id):
                company_trending = trending_list
                break

        if not company_trending:
            return ret  # impossible

        item_id, rows = company_trending.split("^")
        for row in rows.split(";"):
            if not row:
                continue
            row = row.split("|")
            item = TrendingItem()
            item.detail_item_id = int(item_id)
            item.host_win = round(float(row[0]), 2)
            item.draw = round(float(row[1]), 2)
            item.guest_win = round(float(row[2]), 2)
            item.change_time = datetime.strptime(f"{self._this_year}-{row[3]}",
                                                 "%Y-%m-%d %H:%M")  # row[3] == '04-05 07:59'
            item.kali_low = round(float(row[4]), 2)
            item.kali_mid = round(float(row[5]), 2)
            item.kali_high = round(float(row[6]), 2)
            ret.append(item)
        return ret

    def _extract_meta_item(self, elem: Element) -> MetaItem:
        item = MetaItem()
        item.league_name = elem.xpath("td[1]/text()")[0]
        date_time = elem.xpath("td[2]/text()")[0]  # "03-20 22:00"
        item.league_time = datetime.strptime(f"{self._this_year}-{date_time}", "%Y-%m-%d %H:%M")
        home_team = elem.xpath('td[@class="team"][1]/a//text()')
        item.home_team = "".join(home_team).strip()
        guest_team = elem.xpath('td[@class="team"][2]/a//text()')
        item.guest_team = "".join(guest_team).strip()
        item.score = elem.xpath('.//font[@color="red"]/text()')[0]
        company_num = elem.xpath('td[@class="gocheck"]/text()')[0]
        item.company_num = int(company_num.strip("()"))
        item.detail_url = elem.xpath('td[@class="gocheck"]/a/@href')[0]  # "2137086.htm"
        # game data
        game_data_1 = elem.xpath(".//td[position()>=4 and position()<=6]/text()")  # ["7.51","3.61","1.43"]
        game_data_1 = [round(float(i), 2) for i in game_data_1]
        item.host_win1, item.draw1, item.guest_win1 = game_data_1
        game_data_2 = elem.xpath("following-sibling::tr[1]//td/text()")[:3]  # maybe []
        game_data_2 = [round(float(i), 2) for i in game_data_2] or [0, 0, 0]
        item.host_win2, item.draw2, item.guest_win2 = game_data_2
        return item

    async def _parse(self, date: str):
        async for meta in self._parse_meta_item(date):
            # skip if we have parsed yet
            if self._history.contains(meta):
                continue
            self._history.add(meta)

            if not self._strategy.is_meta_useful(meta):
                continue

            detail = await self._parse_detail_info(meta)
            if self._strategy.worth_push(detail):
                self._meta_queue.put(meta)

            # insert meta and detail info to db
            if self._strategy.worth_store(detail):
                self._db.append(detail)

    async def start(self, *, utc_date: datetime = None):
        utc_date = utc_date or datetime.utcnow()
        utc_str = utc_date.strftime("%Y-%m-%d")
        self._this_year = str(utc_date.year)

        logger.info(f"{'=' * 50} Task running {'=' * 50}")
        logger.info(f"Date now: [UTC] {utc_str}")

        # load history
        self._history.load()
        # wait proxy pool ready
        self.wait_proxy_available()
        # start parse
        await self._parse(utc_str)
        # save parse history
        self._history.save()

        logger.info(f"{'=' * 50} Task finished {'=' * 50}\n\n")

        if self._close_session_after_parse:
            await self.close_session()
