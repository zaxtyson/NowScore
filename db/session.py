from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import db_host, db_username, db_password, db_name
from db.model import DetailInfo, Base
from utils.logger import logger


class SqlSession:

    def __init__(self):
        db_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}?charset=utf8mb4"
        self._engine = create_engine(db_url, echo=False)
        self._session = Session(self._engine)
        Base.metadata.create_all(self._engine)  # create table if not exists

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SqlSession, cls).__new__(cls)
        return cls.instance

    def append(self, detail: DetailInfo):
        self._session.add(detail.meta)
        for item in detail.items:
            self._session.add(item)

    def commit(self):
        try:
            logger.info("Commit to database...")
            self._session.commit()
        except Exception as e:
            logger.error(f"Commit to db failed: {e}")

    def close(self):
        self._session.close()
