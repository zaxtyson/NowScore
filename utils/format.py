from typing import List
from core.model import LeagueMetaInfo


def make_simple_message(meta_list: List[LeagueMetaInfo]) -> str:
    message = "联赛名\t时间\t主队名\t客队名"
    for meta in meta_list:
        message += f"\n{meta.name}\t{meta.time}\t{meta.home_team}\t{meta.guest_team}"
    return message


def make_markdown_message(meta_list: List[LeagueMetaInfo]) -> str:
    message = "|联赛名|时间|主队名|客队名|"
    message += "\n| :-: | :-: | :-: |:-:|"
    for meta in meta_list:
        message += f"\n|{meta.name}|{meta.time}|{meta.home_team}|{meta.guest_team}|"
    message = message.replace("[", "\\[")
    return message
