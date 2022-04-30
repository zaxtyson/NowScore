import asyncio
from datetime import datetime, timedelta

from spider.spider import NowScoreSpider
from strategy.s_2022_04_28 import SpiderStrategy


async def auto_run(spider: NowScoreSpider):
    start_date = datetime(2021, 4, 1)
    end_date = datetime(2022, 4, 5)

    while start_date.date() != end_date.date():
        await spider.start(utc_date=start_date)
        start_date += timedelta(days=1)

    await spider.close_session()


if __name__ == '__main__':
    spider = NowScoreSpider()
    spider.settings(
        strategy=SpiderStrategy(),
        persistence_history=False,
        enable_proxy_pool=True,
        close_session_after_done=False
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(auto_run(spider))
