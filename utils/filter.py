from config import *
from core.model import LeagueMetaInfo, LeagueDetailInfo


def custom_meta_filter(meta: LeagueMetaInfo) -> bool:
    if meta.company_num < min_company_num:
        return False
    return True


def custom_detail_filter(detail: LeagueDetailInfo) -> bool:
    if detail.state in ["推迟", "错误"]:
        return False
    if any(i >= max_index_avg for i in detail.index_avg):
        return False
    if any(i >= max_index_high for i in detail.index_high):
        return False
    if detail.bet365_host_win < min_bet365_host_win:
        return False
    return True
