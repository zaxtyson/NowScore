import asyncio

from config import wechat_send_keys
from pusher.msg_format import make_markdown_message
from pusher.wechat import WechatPusher
from spider.spider import NowScoreSpider
from strategy.s_2022_03_31 import SpiderStrategy

if __name__ == '__main__':
    spider = NowScoreSpider()
    spider.settings(
        strategy=SpiderStrategy(),
        persistence_history=True,
        enable_proxy_pool=False,
        close_session_after_done=True
    )

    wechat = WechatPusher()
    wechat.set_send_keys(wechat_send_keys)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.start())

    meta_list = spider.get_meta_list()
    if meta_list:
        wechat.push(
            title="NowScoreSpider 推送",
            msg=make_markdown_message(meta_list),
            repeat=10,
            interval=1
        )
