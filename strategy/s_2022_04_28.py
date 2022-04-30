from db.model import DetailInfo, MetaItem
from strategy.base import BaseStrategy, Condition


class SpiderStrategy(BaseStrategy):

    def _is_meta_useful(self, meta: MetaItem) -> bool:
        return meta.company_num >= 60

    def _worth_store(self, detail: DetailInfo) -> bool:
        return detail.bet365 is not None

    def _worth_push(self, detail: DetailInfo) -> bool:
        meta = detail.meta

        # step 1
        c1 = Condition(lambda: meta.company_num >= 60)

        # step 2
        data = [meta.host_win1, meta.draw1, meta.guest_win1, meta.host_win2, meta.draw2, meta.guest_win2]
        c2_1 = Condition(lambda: all(i > 0 for i in data))
        c2_2 = Condition(
            lambda: meta.guest_win2 > meta.guest_win1 > meta.draw2 > meta.draw1 > meta.host_win1 > meta.host_win2)
        c1.add_next(c2_1)
        c2_1.add_next(c2_2)

        # step 3
        c3 = Condition(lambda: detail.state not in ["推迟", "错误"])
        c2_2.add_next(c3)

        # step 4
        c4 = Condition(
            lambda: detail.bet365 and detail.bet365.instant_host_win in [1.4, 1.5, 1.55, 1.7, 1.91, 1.95, 2.05, 2.15,
                                                                         2.25])
        c3.add_next(c4)

        # step 5 (new)
        c5_1 = Condition(
            lambda: detail.bet365.instant_draw in [3.1, 3.2, 3.25, 3.4, 3.5, 3.75, 3.8, 4, 4.33]
        )
        c4.add_next(c5_1)

        # step 5
        c5 = Condition(lambda: all(i < 1.2 for i in [detail.max_kali_low, detail.max_kali_mid, detail.max_kali_high]))
        c5_1.add_next(c5)

        # step 6
        c6 = Condition(
            lambda: all(i >= 0.7 for i in [detail.min_kali_low, detail.min_kali_mid, detail.min_kali_high]))
        c5.add_next(c6)

        # step 7
        c7_1 = Condition(lambda: detail.avg_kali_low == detail.avg_kali_mid == detail.avg_kali_high)
        c7_2 = Condition(
            lambda: all(i < 0.93 for i in [detail.avg_kali_low, detail.avg_kali_mid, detail.avg_kali_high]))
        c6.add_next(c7_1)
        c7_1.add_next(c7_2)

        # step 8
        c8_1 = Condition(lambda: detail.bet365.instant_host_win < detail.initial_avg_host_win)
        c8_2 = Condition(lambda: detail.bet365.instant_host_win < detail.instant_avg_host_win)
        c8_3 = Condition(lambda: detail.bet365.instant_draw > detail.initial_avg_draw)
        c8_4 = Condition(lambda: detail.bet365.instant_draw > detail.instant_avg_draw)
        c8_5 = Condition(lambda: detail.bet365.instant_guest_win > detail.initial_avg_guest_win)
        c8_6 = Condition(lambda: detail.bet365.instant_guest_win > detail.instant_avg_guest_win)
        c7_2.add_next(c8_1)
        c8_1.add_next(c8_2)
        c8_2.add_next(c8_3)
        c8_3.add_next(c8_4)
        c8_4.add_next(c8_5)
        c8_5.add_next(c8_6)

        # step 9
        c9_1 = Condition(lambda: detail.max_kali_low < detail.max_kali_mid < detail.max_kali_high)
        c9_2 = Condition(lambda: detail.max_kali_low < 1 and detail.max_kali_mid >= 1)
        c9_3 = Condition(lambda: detail.min_kali_low > detail.min_kali_mid > detail.min_kali_high)
        c8_6.add_next(c9_1)
        c9_1.add_next(c9_2, c9_3)

        return c1.is_true()
