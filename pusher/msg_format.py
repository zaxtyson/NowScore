from typing import List

from db.model import MetaItem


def make_simple_message(meta_list: List[MetaItem]) -> str:
    message = "联赛名\t时间\t主队名\t客队名"
    for meta in meta_list:
        message += f"\n{meta.league_name}\t{meta.league_time.strftime('%m-%d %H:%M')}\t{meta.home_team}\t{meta.guest_team}"
    return message


def make_markdown_message(meta_list: List[MetaItem]) -> str:
    message = "\n\n|联赛名|时间|主队名|客队名|链接|"
    message += "\n| :-: | :-: | :-: |:-:|:-:|"
    for meta in meta_list:
        uri = f"[查看](http://live.nowscore.com/1x2/{meta.detail_url})"
        message += f"\n|{meta.league_time}|{meta.league_time.strftime('%m-%d %H:%M')}|{meta.home_team}|{meta.guest_team}|{uri}|"
    message = message.replace("[", r"\[")
    message = message.replace(r"\[查看]", "[查看]")
    return message
