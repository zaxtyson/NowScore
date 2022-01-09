from config import send_keys
from core.spider import NowScoreSpider
from core.wechat import WechatPusher
from utils.filter import custom_meta_filter, custom_detail_filter
from utils.format import make_markdown_message
from utils.push_check import PushStrategy

if __name__ == '__main__':
    spider = NowScoreSpider()
    spider.set_meta_filter(custom_meta_filter)
    spider.set_detail_filter(custom_detail_filter)
    spider.set_meta_callback(print)

    wechat = WechatPusher()
    wechat.set_sed_keys(send_keys)
    push_strategy = PushStrategy()

    # Let's start
    spider.run()
    meta_list = spider.get_meta_list()
    if push_strategy.need_push(meta_list):
        msg = make_markdown_message(meta_list)
        wechat.push("NowScoreSpider 推送", msg)
