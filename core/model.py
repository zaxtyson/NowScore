class LeagueMetaInfo:

    def __init__(self):
        self.name = ""
        self.time = ""
        self.home_team = ""
        self.guest_team = ""
        self.score = ""
        self.game_data = []
        self.company_num = 0
        self.detail_url = ""

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


class LeagueDetailInfo:

    def __init__(self):
        self._state = -100
        self.bet365_host_win = 0
        self.bet365_guest_win = 0
        self.index_avg_data = [0, 0, 0, 0, 0, 0]
        self.index_avg_kali = [0, 0, 0]
        self.index_low_data = [0, 0, 0, 0, 0, 0]
        self.index_low_kali = [0, 0, 0]
        self.index_high_data = [0, 0, 0, 0, 0, 0]
        self.index_high_kali = [0, 0, 0]
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

    def __str__(self):
        return str(self.__dict__)
