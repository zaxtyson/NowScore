import json
import os
from typing import List, Set

from core.model import LeagueMetaInfo
from utils.logger import logger


class PushStrategy:
    def __init__(self):
        self._record_file = os.path.dirname(__file__) + "/last_push"

    def _load_last_urls(self) -> Set[str]:
        """Load the detail urls that we had pushed in the last time"""
        with open(self._record_file, "r") as f:
            url_list = json.load(f)
            return set(url_list)

    def _dump_meta_list(self, meta_list: List[LeagueMetaInfo]):
        """Dump the detail url to file"""
        with open(self._record_file, "w") as f:
            url_list = [meta.detail_url for meta in meta_list]
            logger.debug(f"Dump meta detail url list: {url_list}")
            json.dump(url_list, f)

    def push_filter(self, meta_list: List[LeagueMetaInfo]) -> List[LeagueMetaInfo]:
        # last      this         push
        # [1,2,3]   [1,2,3,4] => [4]
        # [1,2,3,4] [1,3,4]   => []
        # [1,2,3]   [1,2,3]   => []

        if not meta_list:
            logger.warn("No data to push")
            return []  # no data

        url_set = {meta.detail_url for meta in meta_list}
        last_push = self._load_last_urls()
        logger.info(f"Pushed last time: {last_push}, url this time: {url_set}")

        # last_push contains/equal url_set
        if last_push.issuperset(url_set):
            logger.warn("No need to push")
            return []

        self._dump_meta_list(meta_list)
        push_set = url_set.difference(last_push)
        logger.info(f"To push: {push_set}")
        return [meta for meta in meta_list if meta.detail_url in push_set]

