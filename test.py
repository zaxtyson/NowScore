from core.spider import NowScoreSpider
from utils.filter import custom_meta_filter, custom_detail_filter

if __name__ == '__main__':
    spider = NowScoreSpider()
    spider.set_meta_filter(custom_meta_filter)
    spider.set_detail_filter(custom_detail_filter)
    spider.set_meta_callback(print)

    # Let's start
    spider.run(date="2022-03-20")
    for meta in spider.get_meta_list():
        print(meta)
