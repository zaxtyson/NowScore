from typing import List
from core.model import LeagueMetaInfo


def make_simple_message(meta_list: List[LeagueMetaInfo]) -> str:
    message = "联赛名\t时间\t主队名\t客队名"
    for meta in meta_list:
        message += f"\n{meta.name}\t{meta.time}\t{meta.home_team}\t{meta.guest_team}"
    return message


def make_markdown_message(meta_list: List[LeagueMetaInfo]) -> str:
    message = "> 网站被微信屏蔽, 请点右上角用浏览器打开"
    message += "\n\n|联赛名|时间|主队名|客队名|链接|"
    message += "\n| :-: | :-: | :-: |:-:|:-:|"
    for meta in meta_list:
        url_text = f"[查看](http://score.nowscore.com/1x2/{meta.detail_url})"
        message += f"\n|{meta.name}|{meta.time}|{meta.home_team}|{meta.guest_team}|{url_text}|"
    message = message.replace("[", r"\[")
    message = message.replace(r"\[查看]", "[查看]")
    return message
