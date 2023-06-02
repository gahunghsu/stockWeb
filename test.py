import yfinance as yf
import pandas as pd

# 歷史價格
# data = yf.Ticker("2330.TW")
# df = data.history(period="max")

# 获取股票历史数据
symbol = "2330.TW"  # 股票代码
start_date = "2023-06-02"  # 开始日期
end_date = "2023-06-02"  # 结束日期

data = yf.download(symbol, start=start_date, end=end_date)
print(data)

# print(df)
# 買賣超
# https://www.twse.com.tw/fund/T86?response=json&date=20230601&selectType=ALL