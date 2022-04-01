from datetime import datetime

from db.model import MetaItem, DetailItem
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
    detail = DetailItem(
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
        kali_high=0.89
    )

    session.append_meta_item(meta)
    session.append_meta_item(detail)
    session.commit()
    session.close()
