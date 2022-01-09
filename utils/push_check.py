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
            logger.debug(f"Pushed last time: {url_list}")
            return set(url_list)

    def _dump_meta_list(self, meta_list: List[LeagueMetaInfo]):
        """Dump the detail url to file"""
        with open(self._record_file, "w") as f:
            url_list = [meta.detail_url for meta in meta_list]
            logger.debug(f"Dump meta detail url list: {url_list}")
            json.dump(url_list, f)

    def need_push(self, meta_list: List[LeagueMetaInfo]) -> bool:
        if not meta_list:
            logger.warn("No data to push")
            return False  # no data

        url_set = {meta.detail_url for meta in meta_list}
        if url_set == self._load_last_urls():
            logger.warn("Same data as last time, no need to push")
            return False

        logger.info(f"{len(meta_list)} items to be pushed")
        self._dump_meta_list(meta_list)
        return True
