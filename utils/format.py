from queue import Queue


def make_simple_message(queue: Queue) -> str:
    message = "联赛名\t时间\t主队名\t客队名"
    while not queue.empty():
        meta = queue.get()
        message += f"\n{meta.name}\t{meta.time}\t{meta.home_team}\t{meta.guest_team}"
    return message


def make_markdown_message(queue: Queue) -> str:
    message = "|联赛名|时间|主队名|客队名|"
    message += "\n| :-: | :-: | :-: |:-:|"
    while not queue.empty():
        meta = queue.get()
        message += f"\n|{meta.name}|{meta.time}|{meta.home_team}|{meta.guest_team}|"
    message = message.replace("[", "\\[")
    return message
