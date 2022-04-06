from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from config import db_host, db_username, db_password, db_name
from db.model import DetailInfo, Base
from utils.logger import logger


class SqlSession:

    def __init__(self):
        db_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}?charset=utf8mb4"
        self._engine = create_engine(db_url, echo=False)
        self._session = Session(self._engine)
        self._to_submit_meta_items = 0
        self._to_submit_detail_items = 0
        self._to_submit_trending_items = 0
        if not inspect(self._engine).has_table("detail_statistic"):
            Base.metadata.create_all(self._engine)  # create table if not exists

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SqlSession, cls).__new__(cls)
        return cls.instance

    def append(self, detail: DetailInfo):
        self._session.add(detail.meta)
        self._to_submit_meta_items += 1
        for item in detail.items:
            self._session.add(item)
            self._to_submit_detail_items += 1
            for trending in item.trending_list:
                self._session.add(trending)
                self._to_submit_trending_items += 1
        self.commit()

    def commit(self):
        try:
            if self._to_submit_meta_items > 0:
                logger.info(f"Commit to database, {self._to_submit_meta_items} meta item(s), "
                            f"{self._to_submit_detail_items} detail item(s), "
                            f"{self._to_submit_trending_items} trending item(s)...")
                self._to_submit_meta_items = 0
                self._to_submit_detail_items = 0
                self._to_submit_trending_items = 0
                self._session.commit()
        except Exception as e:
            logger.error(f"Commit to db failed: {e}")
            self._session.rollback()

    def close(self):
        self._session.close()
