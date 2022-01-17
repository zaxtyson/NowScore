from config import *
from core.model import LeagueMetaInfo, LeagueDetailInfo
import datetime


def is_today(date: str):
    # format '01-15 08:00'
    today = datetime.datetime.now()
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


def custom_meta_filter(meta: LeagueMetaInfo) -> bool:
    if meta.company_num < min_company_num:
        return False
    if not is_today(meta.time):
        return False
    return True


def custom_detail_filter(detail: LeagueDetailInfo) -> bool:
    # Base condition
    if detail.state in ["推迟", "错误"]:
        return False
    if any(i >= max_index_avg for i in detail.index_avg):
        return False
    if any(i >= max_index_high for i in detail.index_high):
        return False
    if detail.bet365_host_win < min_bet365_host_win:
        return False

    # Target condition
    if is_upward(detail.index_high) and detail.index_high[0] < 1:
        if not enable_mid_value_filter:
            return True
        # do more check
        if detail.index_high[1] >= 1:
            return True
    if is_upward(detail.index_high) and is_downward(detail.index_low):
        return True
    if is_upward(detail.index_high) and is_upward(detail.index_low):
        return True
    return False
