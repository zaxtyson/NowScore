# NowScoreSpider

抓取 [捷报比分 > 足球比分 > 完场回查](http://score.nowscore.com/1x2/bet007history.htm) 的数据, 推送到微信

## 使用说明

- 安装 `Python3.6+`, 在命令行下执行 `python3 -m pip install -r requirements.txt` 安装依赖

- 使用 `python3 main.py` 运行程序, 数据抓取完成存储到数据库, 满足策略的比赛即时推送到微信 

- 微信推送使用 [Server酱](https://sct.ftqq.com/login), 扫码登陆, 复制 `SendKey` 到 `config.py` 即可

- 定时任务请使用 `crontab` 添加