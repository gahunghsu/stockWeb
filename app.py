import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
from random import randint

class StockPriceAmount:
    def __init__(self, symbol, date, open_price, high_price, low_price, close_price, amount,
                 foreign_investment, mutual_fund, proprietary_trading, total,
                 foreign_investment_percentage, margin_trading_change, margin_trading_balance,
                 short_selling_change, short_selling_balance, equity_margin_ratio):
        self.symbol = symbol
        self.date = date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.amount = amount
        self.foreign_investment = foreign_investment
        self.mutual_fund = mutual_fund
        self.proprietary_trading = proprietary_trading
        self.total = total
        self.foreign_investment_percentage = foreign_investment_percentage
        self.margin_trading_change = margin_trading_change
        self.margin_trading_balance = margin_trading_balance
        self.short_selling_change = short_selling_change
        self.short_selling_balance = short_selling_balance
        self.equity_margin_ratio = equity_margin_ratio

def create_stock_price_amount_table():
    # 建立資料庫連線
    conn = sqlite3.connect('stockdb.db')

    # 建立資料庫游標
    cursor = conn.cursor()

    # 建立 stock_price 資料表
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS stock_price_amount (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        symbol TEXT,
        open_price REAL,
        high_price REAL,
        low_price REAL,
        close_price REAL,
        amount REAL,
        foreign_investment REAL,
        mutual_fund REAL,
        proprietary_trading REAL,
        total REAL,
        foreign_investment_percentage REAL,
        margin_trading_change INTEGER,
        margin_trading_balance INTEGER,
        short_selling_change INTEGER,
        short_selling_balance INTEGER,
        equity_margin_ratio REAL
    )
    '''
    cursor.execute(create_table_query)

    # 提交變更
    conn.commit()

    # 關閉連線
    conn.close()  

def insert_stock_price_amount(stock_proce_amount_obj):
    # 建立資料庫連線
    conn = sqlite3.connect('stockdb.db')

    # 建立資料庫游標
    cursor = conn.cursor()

    # 解析 stock_proce_amount_obj 对象的属性
    symbol = stock_proce_amount_obj.symbol
    date = stock_proce_amount_obj.date
    open_price = stock_proce_amount_obj.open_price
    high_price = stock_proce_amount_obj.high_price
    low_price = stock_proce_amount_obj.low_price
    close_price = stock_proce_amount_obj.close_price
    amount = stock_proce_amount_obj.amount
    foreign_investment = stock_proce_amount_obj.foreign_investment
    mutual_fund = stock_proce_amount_obj.mutual_fund
    proprietary_trading = stock_proce_amount_obj.proprietary_trading
    total = stock_proce_amount_obj.total
    foreign_investment_percentage = stock_proce_amount_obj.foreign_investment_percentage
    margin_trading_change = stock_proce_amount_obj.margin_trading_change
    margin_trading_balance = stock_proce_amount_obj.margin_trading_balance
    short_selling_change = stock_proce_amount_obj.short_selling_change
    short_selling_balance = stock_proce_amount_obj.short_selling_balance
    equity_margin_ratio = stock_proce_amount_obj.equity_margin_ratio

    # 檢查是否已存在相同的 symbol 和 date
    select_query = '''
    SELECT COUNT(*) FROM stock_price_amount WHERE symbol = ? AND date = ?
    '''
    cursor.execute(select_query, (symbol, date))
    result = cursor.fetchone()

    if result[0] > 0:
        # 如果存在相同的 symbol 和 date，先刪除該筆資料
        delete_query = '''
        DELETE FROM stock_price_amount WHERE symbol = ? AND date = ?
        '''
        cursor.execute(delete_query, (symbol, date))

    # 插入資料到 stock_price_amount 資料表
    insert_query = '''
    INSERT INTO stock_price_amount (
        symbol, open_price, high_price, low_price, close_price, amount, date,
        foreign_investment, mutual_fund, proprietary_trading, total,
        foreign_investment_percentage, margin_trading_change, margin_trading_balance,
        short_selling_change, short_selling_balance, equity_margin_ratio
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(insert_query, (
        symbol, open_price, high_price, low_price, close_price, amount, date,
        foreign_investment, mutual_fund, proprietary_trading, total,
        foreign_investment_percentage, margin_trading_change, margin_trading_balance,
        short_selling_change, short_selling_balance, equity_margin_ratio
    ))

    # 提交變更
    conn.commit()

    # 關閉連線
    conn.close()

def get_stock_price(symbol, type):
    url = f"https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID={symbol}&CHT_CAT2=DATE"
    
    # 建立Session物件並設置User-Agent
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'    
    response = session.get(url)
    response.encoding = 'utf-8'  # 指定正確的編碼
    soup = BeautifulSoup(response.text, "html.parser")
    table_elements = soup.find_all("table", attrs={"id": "tblPriceDetail"})
    if table_elements:
        table_element = table_elements[0]  # 使用索引獲取第一個元素                
        tr_elements = table_element.find_all("tr", attrs={"align": "center"})        
        for tr_element in tr_elements:
            td_elements = tr_element.find_all("td")
            date = td_elements[0].text
            open = td_elements[1].text
            high = td_elements[2].text
            low = td_elements[3].text
            close = td_elements[4].text
            amount = td_elements[8].text
            foreign_investment = td_elements[12].text
            mutual_fund = td_elements[13].text
            proprietary_trading = td_elements[14].text
            total = td_elements[15].text
            foreign_investment_percentage = td_elements[16].text
            margin_trading_change = td_elements[17].text
            margin_trading_balance = td_elements[18].text
            short_selling_change= td_elements[19].text
            short_selling_balance= td_elements[20].text
            equity_margin_ratio= td_elements[21].text
            # 取得當前年份
            current_year = datetime.now().year
            # 创建 StockPriceAmount 对象
            stock_proce_amount_obj = StockPriceAmount(symbol, f"{current_year}/{date}", open, high, low, close, amount,
                                                      foreign_investment, mutual_fund, proprietary_trading, total,
                                                      foreign_investment_percentage, margin_trading_change,
                                                      margin_trading_balance, short_selling_change,
                                                      short_selling_balance, equity_margin_ratio)

            # 插入数据到数据库
            insert_stock_price_amount(stock_proce_amount_obj)
            if type == "now":
                break

def get_stock_symbols(market):
    if market == "TWSE":
        url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
        code_key = "Code"
    else:
        url = "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes"
        code_key = "SecuritiesCompanyCode"
    response = requests.get(url)
    data = response.json()

    symbols = [item[code_key] for item in data]
    
    return symbols

if __name__ == "__main__":
    create_stock_price_amount_table()
    twse_symbols = get_stock_symbols("TWSE")
    tpex_symbols = get_stock_symbols("TPEx")
    merged_symbols = twse_symbols + tpex_symbols
    for symbol in merged_symbols:
        delay = randint(1, 5)  # 随机延迟1到5秒
        time.sleep(delay)
        get_stock_price(symbol, "hist")