from statistics import mean
from typing import List, Optional

from cached_property import cached_property
from sqlalchemy import Column, String, DECIMAL, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MetaItem(Base):
    __tablename__ = "meta"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    detail_url = Column(String(20), unique=True, index=True, nullable=False, comment="详情页链接")
    league_name = Column(String(30), nullable=False, comment="联赛名称")
    league_time = Column(DateTime, nullable=False, comment="联赛时间")
    home_team = Column(String(30), nullable=False, comment="主队名")
    guest_team = Column(String(30), nullable=False, comment="客队名")
    score = Column(String(10), nullable=False, comment="比分")
    company_num = Column(Integer, nullable=False, comment="公司数量")
    host_win1 = Column(DECIMAL(5, 2), nullable=False, comment="主胜-上")
    host_win2 = Column(DECIMAL(5, 2), nullable=False, comment="主胜-下")
    draw1 = Column(DECIMAL(5, 2), nullable=False, comment="和局-上")
    draw2 = Column(DECIMAL(5, 2), nullable=False, comment="和局-下")
    guest_win1 = Column(DECIMAL(5, 2), nullable=False, comment="客胜-上")
    guest_win2 = Column(DECIMAL(5, 2), nullable=False, comment="客胜-下")

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items() if k not in ["_sa_instance_state"]})

    def __repr__(self):
        return self.__str__()


class DetailItem(Base):
    __tablename__ = "detail"

    item_id = Column(Integer, primary_key=True, unique=True, comment="该条数据的id")
    detail_url = Column(String(20), nullable=False, index=True, comment="详情页链接")
    company_name_en = Column(String(30), nullable=False, comment="公司英文名")
    company_name_zh = Column(String(30), nullable=False, comment="公司中文名")
    initial_host_win = Column(DECIMAL(5, 2), nullable=False, comment="初指-主胜")
    initial_draw = Column(DECIMAL(5, 2), nullable=False, comment="初指-和局")
    initial_guest_win = Column(DECIMAL(5, 2), nullable=False, comment="初指-客胜")
    initial_return_rate = Column(DECIMAL(5, 2), nullable=False, comment="初指-返还率")
    instant_host_win = Column(DECIMAL(5, 2), nullable=False, comment="即时-主胜")
    instant_draw = Column(DECIMAL(5, 2), nullable=False, comment="即时-和局")
    instant_guest_win = Column(DECIMAL(5, 2), nullable=False, comment="即时-客胜")
    instant_return_rate = Column(DECIMAL(5, 2), nullable=False, comment="即时-返还率")
    kali_low = Column(DECIMAL(3, 2), nullable=False, comment="凯利指数-低")
    kali_mid = Column(DECIMAL(3, 2), nullable=False, comment="凯利指数-中")
    kali_high = Column(DECIMAL(3, 2), nullable=False, comment="凯利指数-高")
    is_main_company = Column(Boolean, nullable=False, default=False, comment="是否主流公司")
    is_exchange = Column(Boolean, nullable=False, default=False, comment="是否交易所")
    trending_list = []

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items() if k not in ["_sa_instance_state", "trending_list"]})

    def __repr__(self):
        return self.__str__()


class TrendingItem(Base):
    __tablename__ = "trending"

    id = Column(Integer, primary_key=True, unique=True)
    detail_item_id = Column(Integer, nullable=False, index=True)
    host_win = Column(DECIMAL(5, 2), nullable=False, comment="主胜")
    draw = Column(DECIMAL(5, 2), nullable=False, comment="和局")
    guest_win = Column(DECIMAL(5, 2), nullable=False, comment="客胜")
    change_time = Column(DateTime, nullable=False, comment="变化时间")
    kali_low = Column(DECIMAL(3, 2), nullable=False, comment="凯利指数-低")
    kali_mid = Column(DECIMAL(3, 2), nullable=False, comment="凯利指数-中")
    kali_high = Column(DECIMAL(3, 2), nullable=False, comment="凯利指数-高")

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items() if k not in ["_sa_instance_state"]})

    def __repr__(self):
        return self.__str__()


class DetailInfo:

    def __init__(self):
        self._state = -100
        self.items: List[DetailItem] = []
        self.meta = None

    @property
    def state(self):
        state_map = {-14: "推迟", -13: "中断", -12: "腰砍", -11: "待定", -10: "取消", -1: "完场",
                     0: "未开场", 1: "上半场", 2: "中场", 3: "下半场", 4: "加时", 5: "点球"}
        if self._state not in state_map.keys():
            return "错误"
        return state_map[self._state]

    @state.setter
    def state(self, value: int):
        self._state = value

    # bet365
    @cached_property
    def bet365(self) -> Optional[DetailItem]:
        for i in self.items:
            if i.company_name_en == "Bet 365":
                return i
        return None

    # kali index
    @cached_property
    def max_kali_low(self):
        return max(i.kali_low for i in self.items)

    @cached_property
    def max_kali_mid(self):
        return max(i.kali_mid for i in self.items)

    @cached_property
    def max_kali_high(self):
        return max(i.kali_high for i in self.items)

    @cached_property
    def min_kali_low(self):
        return min(i.kali_low for i in self.items)

    @cached_property
    def min_kali_mid(self):
        return min(i.kali_mid for i in self.items)

    @cached_property
    def min_kali_high(self):
        return min(i.kali_high for i in self.items)

    @cached_property
    def avg_kali_low(self):
        return round(mean(i.kali_low for i in self.items), 2)

    @cached_property
    def avg_kali_mid(self):
        return round(mean(i.kali_mid for i in self.items), 2)

    @cached_property
    def avg_kali_high(self):
        return round(mean(i.kali_high for i in self.items), 2)

    # initial index max
    @cached_property
    def initial_max_host_win(self):
        return max(i.initial_host_win for i in self.items)

    @cached_property
    def initial_max_draw(self):
        return max(i.initial_draw for i in self.items)

    @cached_property
    def initial_max_guest_win(self):
        return max(i.initial_guest_win for i in self.items)

    @cached_property
    def initial_max_return_rate(self):
        return max(i.initial_return_rate for i in self.items)

    # instant index max
    @cached_property
    def instant_max_host_win(self):
        return max(i.instant_host_win for i in self.items)

    @cached_property
    def instant_max_draw(self):
        return max(i.instant_draw for i in self.items)

    @cached_property
    def instant_max_guest_win(self):
        return max(i.instant_guest_win for i in self.items)

    @cached_property
    def instant_max_return_rate(self):
        return max(i.instant_return_rate for i in self.items)

    # initial index min
    @cached_property
    def initial_min_host_win(self):
        return min(i.initial_host_win for i in self.items)

    @cached_property
    def initial_min_draw(self):
        return min(i.initial_draw for i in self.items)

    @cached_property
    def initial_min_guest_win(self):
        return min(i.initial_guest_win for i in self.items)

    @cached_property
    def initial_min_return_rate(self):
        return min(i.initial_return_rate for i in self.items)

    # instant index min
    @cached_property
    def instant_min_host_win(self):
        return min(i.instant_host_win for i in self.items)

    @cached_property
    def instant_min_draw(self):
        return min(i.instant_draw for i in self.items)

    @cached_property
    def instant_min_guest_win(self):
        return min(i.instant_guest_win for i in self.items)

    @cached_property
    def instant_min_return_rate(self):
        return min(i.instant_return_rate for i in self.items)

    # initial index avg
    @cached_property
    def initial_avg_host_win(self):
        return round(mean(i.initial_host_win for i in self.items), 2)

    @cached_property
    def initial_avg_draw(self):
        return round(mean(i.initial_draw for i in self.items), 2)

    @cached_property
    def initial_avg_guest_win(self):
        return round(mean(i.initial_guest_win for i in self.items), 2)

    @cached_property
    def initial_avg_return_rate(self):
        return round(mean(i.initial_return_rate for i in self.items), 2)

    # instant index avg
    @cached_property
    def instant_avg_host_win(self):
        return round(mean(i.instant_host_win for i in self.items), 2)

    @cached_property
    def instant_avg_draw(self):
        return round(mean(i.instant_draw for i in self.items), 2)

    @cached_property
    def instant_avg_guest_win(self):
        return round(mean(i.instant_guest_win for i in self.items), 2)

    @cached_property
    def instant_avg_return_rate(self):
        return round(mean(i.instant_return_rate for i in self.items), 2)

    def __str__(self):
        d = {k: v for k, v in self.__dict__.items() if k not in ["items", "_state"]}
        d.update({"bet365": self.bet365, "state": self.state})
        return str(d)

    def __repr__(self):
        return self.__str__()
