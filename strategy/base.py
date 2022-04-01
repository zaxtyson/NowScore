from db.model import DetailInfo, MetaItem
from utils.logger import logger


class Condition:
    def __init__(self, func):
        self._func = func
        self._value = None
        self._sub_cond = []

    def is_true(self):
        # delay calculate
        if self._value is None:
            self._value = self._func()
        # this node is `False`, the DAG is `False`
        if not self._value:
            return False
        # this node is `True` and not sub-condition, the DAG is `True`
        if not self._sub_cond:
            return True
        # this node is `True` and has sub-condition to calculate
        for cond in self._sub_cond:
            # if any sub-condition is `True`, the DAG is `True`
            if cond.is_true():
                return True
        return False

    def add_next(self, *cond_list):
        for cond in cond_list:
            self._sub_cond.append(cond)

    def clear(self):
        self._value = None
        self._sub_cond.clear()

    def __repr__(self):
        return str(self.__dict__)


class BaseStrategy:

    def _worth_store(self, detail: DetailInfo) -> bool:
        """override this method"""
        return True

    def _worth_push(self, detail: DetailInfo) -> bool:
        """override this method"""
        return True

    def _is_meta_useful(self, meta: MetaItem) -> bool:
        """override this method"""
        return True

    def is_meta_useful(self, meta: MetaItem) -> bool:
        if self._is_meta_useful(meta):
            return True
        logger.info(f"Drop meta item {meta}")
        return False

    def worth_store(self, detail: DetailInfo) -> bool:
        if self._worth_store(detail):
            logger.info(f"Store detail data {detail}")
            return True
        return False

    def worth_push(self, detail: DetailInfo) -> bool:
        if self._worth_push(detail):
            logger.info(f"Push detail data {detail}")
            return True
        return False
