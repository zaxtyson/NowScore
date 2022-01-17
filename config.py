# Server 酱 SendKey, 用于推送消息
send_keys = [
    "SCT1107...0mV2FzFQ"
]

# 公司数 < 此值 时数据将被丢弃
min_company_num = 60

# 初指平均值 >= 此值 时数据将被丢弃
max_index_avg = 0.93

# 初指最高值 >= 此值 时数据将被丢弃
max_index_high = 1.2

# Bet365主胜 < 此值 时数据将被丢弃
min_bet365_host_win = 1.6

# 初指最高值满足递增趋势时, 是否启用"中值 >= 1"这个条件
enable_mid_value_filter = True
