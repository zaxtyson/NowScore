# NowScoreSpider

抓取 [捷报比分 > 足球比分 > 完场回查](http://score.nowscore.com/1x2/bet007history.htm) 的数据, 推送到微信

## 使用说明

- 安装 `Python3`, 在命令行下执行 `python3 -m pip install -r requirements.txt` 安装依赖

- 使用 `python3 main.py` 运行程序, 数据抓取完成后自动推送到微信

- 微信推送使用 [Server酱](https://sct.ftqq.com/login), 扫码登陆, 复制 `SendKey` 到 `config.py` 即可

- 数据过滤规则可在 `config.py` 中配置, 如需更灵活的筛选规则, 可自己实现 `filter` 函数(见 `utils/filter.py`)

## 效果

> 微信推送

![wechat](https://s4.ax1x.com/2022/01/09/7ihPx0.jpg)
