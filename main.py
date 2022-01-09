from config import send_keys
from core.spider import NowScoreSpider
from core.wechat import WechatPusher
from utils.filter import custom_meta_filter, custom_detail_filter
from utils.format import make_markdown_message
from utils.logger import logger

if __name__ == '__main__':
    spider = NowScoreSpider()
    spider.set_meta_filter(custom_meta_filter)
    spider.set_detail_filter(custom_detail_filter)
    spider.set_meta_callback(print)

    wechat = WechatPusher()
    wechat.set_sed_keys(send_keys)

    # Let's start
    spider.run()
    all_meta = spider.get_meta_queue()
    if all_meta.empty():
        logger.warn("No data to push")
        exit(0)

    msg = make_markdown_message(all_meta)
    wechat.push("NowScoreSpider 推送", msg)
