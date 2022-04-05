from datetime import datetime

from db.model import MetaItem, DetailItem, DetailInfo, TrendingItem
from db.session import SqlSession

if __name__ == '__main__':
    session = SqlSession()

    meta = MetaItem(
        league_name="LeagueName01",
        league_time=datetime.now(),
        home_team="HomeTeam01",
        guest_team="GuestTeam01",
        score="2-0",
        company_num=88,
        detail_url="2183509.htm",
        host_win1=5.06,
        host_win2=5.18,
        draw1=3.86,
        draw2=3.87,
        guest_win1=1.52,
        guest_win2=1.52
    )

    detail_item = DetailItem(
        item_id=110475827,
        detail_url="2183509.htm",
        company_name_en="Bet 365",
        company_name_zh="365(英国)",
        initial_host_win=4.00,
        initial_draw=3.80,
        initial_guest_win=1.67,
        initial_return_rate=89.93,
        instant_host_win=5.25,
        instant_draw=4.00,
        instant_guest_win=1.50,
        instant_return_rate=90.32,
        kali_low=0.91,
        kali_mid=0.93,
        kali_high=0.89,
        is_main_company=True,
        is_exchange=False,
    )

    trending_list = [[110475827, 1.75, 3.6, 4.75, datetime(2022, 4, 5, 7, 59), 0.86, 0.99, 1.12],
                     [110475827, 1.75, 3.6, 4.5, datetime(2022, 4, 5, 7, 8), 0.86, 0.99, 1.06],
                     [110475827, 1.85, 3.5, 4.33, datetime(2022, 4, 5, 7, 7), 0.91, 0.96, 1.02],
                     [110475827, 1.85, 3.5, 4.2, datetime(2022, 4, 5, 7, 7), 0.91, 0.96, 0.99],
                     [110475827, 1.8, 3.6, 4.5, datetime(2022, 4, 5, 7, 6), 0.88, 0.99, 1.06],
                     [110475827, 1.85, 3.5, 4.33, datetime(2022, 4, 5, 7, 5), 0.91, 0.96, 1.02],
                     [110475827, 1.75, 3.6, 4.5, datetime(2022, 4, 5, 7, 5), 0.86, 0.99, 1.06],
                     [110475827, 1.85, 3.5, 4.33, datetime(2022, 4, 5, 7, 4), 0.91, 0.96, 1.02],
                     [110475827, 1.8, 3.6, 4.5, datetime(2022, 4, 5, 7, 4), 0.88, 0.99, 1.06],
                     [110475827, 1.85, 3.5, 4.33, datetime(2022, 4, 5, 6, 41), 0.91, 0.96, 1.02],
                     [110475827, 1.75, 3.6, 4.75, datetime(2022, 4, 5, 6, 38), 0.86, 0.99, 1.12],
                     [110475827, 1.85, 3.5, 4.33, datetime(2022, 4, 5, 6, 37), 0.91, 0.96, 1.02],
                     [110475827, 1.75, 3.6, 4.75, datetime(2022, 4, 5, 6, 11), 0.86, 0.99, 1.12],
                     [110475827, 1.85, 3.5, 4.2, datetime(2022, 4, 5, 4, 24), 0.91, 0.96, 0.99],
                     [110475827, 1.91, 3.4, 4.0, datetime(2022, 4, 5, 3, 8), 0.94, 0.93, 0.94],
                     [110475827, 2.0, 3.4, 3.75, datetime(2022, 4, 5, 2, 22), 0.98, 0.93, 0.88],
                     [110475827, 1.91, 3.4, 4.0, datetime(2022, 4, 4, 20, 7), 0.94, 0.93, 0.94],
                     [110475827, 1.95, 3.4, 4.0, datetime(2022, 4, 4, 20, 5), 0.96, 0.93, 0.94],
                     [110475827, 2.05, 3.3, 3.75, datetime(2022, 4, 4, 19, 15), 1.0, 0.91, 0.88],
                     [110475827, 2.1, 3.3, 3.6, datetime(2022, 4, 4, 18, 51), 1.03, 0.91, 0.85],
                     [110475827, 2.3, 3.2, 3.2, datetime(2022, 4, 4, 18, 27), 1.13, 0.88, 0.75],
                     [110475827, 2.3, 3.25, 3.2, datetime(2022, 4, 4, 18, 11), 1.13, 0.89, 0.75],
                     [110475827, 1.91, 3.5, 4.2, datetime(2022, 4, 4, 16, 15), 0.94, 0.96, 0.99],
                     [110475827, 1.83, 3.5, 4.33, datetime(2022, 4, 4, 15, 10), 0.9, 0.96, 1.02],
                     [110475827, 1.91, 3.5, 4.0, datetime(2022, 4, 1, 9, 52), 0.94, 0.96, 0.94],
                     [110475827, 1.85, 3.4, 3.6, datetime(2022, 3, 29, 20, 0), 0.91, 0.93, 0.85]]

    for trending in trending_list:
        item = TrendingItem()
        item.detail_item_id = trending[0]
        item.host_win = trending[1]
        item.draw = trending[2]
        item.guest_win = trending[3]
        item.change_time = trending[4]
        item.kali_low = trending[5]
        item.kali_mid = trending[6]
        item.kali_high = trending[7]
        detail_item.trending_list.append(item)

    detail = DetailInfo()
    detail.state = -1
    detail.meta = meta
    detail.items.append(detail_item)

    session.append(detail)
    session.commit()
    session.close()
