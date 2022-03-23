from config import *
from core.model import LeagueMetaInfo, LeagueDetailInfo
import datetime


def is_today(date: str, debug_date=""):
    # format '01-15 08:00'
    today = datetime.datetime.now()
    if debug_date:
        today = datetime.datetime.strptime(debug_date, "%Y-%m-%d")
    target = datetime.datetime.strptime(date, "%m-%d %H:%M")
    if today.month == target.month and today.day == target.day:
        return True
    return False


def is_upward(data: list):
    last = float("-inf")
    for i in data:
        if i > last:
            last = i
        else:
            return False
    return True


def is_downward(data: list):
    last = float("inf")
    for i in data:
        if i < last:
            last = i
        else:
            return False
    return True


def custom_meta_filter(meta: LeagueMetaInfo, debug_date="") -> bool:
    if not is_today(meta.time, debug_date):
        return False
    if meta.company_num < min_company_num:
        return False
    # check game data validation
    if len(meta.game_data) != 6:
        return False

    D = meta.game_data
    if D[5] > D[2] > D[1] > D[4] > D[0] > D[3]:
        return True
    if D[5] > D[2] > D[4] > D[1] > D[0] > D[3]:
        return True
    # others
    return False


def custom_detail_filter(detail: LeagueDetailInfo) -> bool:
    # Base condition
    if detail.state in ["推迟", "错误"]:
        return False
    if detail.bet365_host_win < min_bet365_host_win:
        return False
    if any(i >= max_index_high for i in detail.index_high_kali):
        return False
    if any(i < min_index_low for i in detail.index_low_kali):
        return False
    if len(set(i for i in detail.index_avg_kali)) != 1:
        return False
    if any(i >= max_index_avg for i in detail.index_avg_kali):
        return False
    # step 8
    if detail.bet365_host_win >= detail.index_avg_data[0]:
        return False
    if detail.bet365_sum <= detail.index_avg_data[1]:
        return False
    if detail.bet365_guest_win <= detail.index_avg_data[2]:
        return False

    # Target condition
    if is_upward(detail.index_high_kali) and detail.index_high_kali[0] < 1:
        if not enable_mid_value_filter:
            return True
        # do more check
        if detail.index_high_kali[1] >= 1:
            return True
    if is_upward(detail.index_high_kali) and is_downward(detail.index_low_kali):
        return True
    return False
