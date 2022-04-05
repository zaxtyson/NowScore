import asyncio
import random
from datetime import datetime, timedelta

from spider.spider import NowScoreSpider
from strategy.s_2022_03_31 import SpiderStrategy


async def auto_run(spider: NowScoreSpider):
    start_date = datetime(2021, 12, 1)
    end_date = datetime(2022, 4, 3)

    while start_date.date() != end_date.date():
        await spider.start(start_date)
        await asyncio.sleep(random.randint(60, 200))
        start_date += timedelta(days=1)


if __name__ == '__main__':
    spider = NowScoreSpider()
    spider.set_strategy(SpiderStrategy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(auto_run(spider))
