import asyncio

from config import wechat_send_keys, wechat_push_repeat, wechat_push_interval
from pusher.msg_format import make_markdown_message
from pusher.wechat import WechatPusher
from spider.spider import NowScoreSpider
from strategy.s_2022_03_31 import SpiderStrategy

if __name__ == '__main__':
    spider = NowScoreSpider()
    spider.set_strategy(SpiderStrategy())

    wechat = WechatPusher()
    wechat.set_send_keys(wechat_send_keys)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.start(close_after_done=True))

    meta_list = spider.get_meta_list()
    if meta_list:
        msg = make_markdown_message(meta_list)
        wechat.push("NowScoreSpider 推送", msg, repeat=wechat_push_repeat, interval=wechat_push_interval)
