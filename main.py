import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import akshare as ak
import dateutil
import datetime

CASH = 100000
START_DATE = '2015-01-07'
END_DATE = '2017-01-07'
trade_cal = pd.read_csv('trade_date.csv')
class Context:
    def __init__(self,cash,start_date,end_date):
        self.cash = cash 
        self.start_date = start_date
        self.end_date = end_date 
        self.positions = {}
        self.benchmark = None 
        self.date_range = trade_cal[(trade_cal['trade_date']>=start_date)& (trade_cal['trade_date']<=end_date)]['trade_date'].values
        self.dt = dateutil.parser.parse(start_date)  #TODO: start_date后一个交易日
class G:
    pass
g = G()


def set_benchmark(security): #只支持一只股票作为基准
    Context.benchmark = security
Context = Context(CASH,START_DATE,END_DATE) 
def attribute_history(security,count,fields=('开盘','收盘','最高','最低')):
    end_date = (Context.dt - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    start_date =  trade_cal[(trade_cal['trade_date']<=end_date)][-count:].iloc[0,:]['trade_date']
    # ToDo: 取值 
    return attribute_daterange_history(security,start_date,end_date,fields)

def attribute_daterange_history(security,start_date,end_date,fields=('开盘','收盘','最高','最低')):
    try:
        f = open(security+'.csv','r')
        df = pd.read_csv(security+'.csv',index_col = '日期',parse_dates=['日期']).loc[start_date:end_date,:]
    except:
        df =  ak.stock_zh_a_hist(security,start_date,end_date, "qfq")
    return df[list(fields)]
def get_today_data(security):
    today = Context.dt
    try:
        f = open(security+'.csv','r', encoding='UTF-8')
        data = pd.read_csv(f,index_col='日期',parse_dates=['日期']).loc[today,:]
    except FileNotFoundError: 
        data = ak.stock_zh_a_hist(security,today,today, "qfq")
    except KeyError: #停牌
        data = pd.Series()
    return data


def _order(today_data,security,amount):
    p = float(today_data['开盘'])
    if len(today_data) == 0:
        print('今日停牌')
        return 
    if Context.cash - amount * p < 0:
        amount = int(Context.cash / p)
        print('现金不足,已调整为%d' %(amount))
    if amount % 100 != 0:
        if amount != -Context.positions.get(security,0):
            amount = int(amount / 100) * 100
            print('不是100的倍数，已调整为%d' %amount)
    if Context.positions.get(security,0) < -amount:
        amount = - Context.positions.get(security,0)
        print('卖出股票不能超过持仓数，已调整为%d' %amount)
    Context.positions[security] = Context.positions.get(security,0) + amount

    Context.cash -= amount * p 
    if Context.positions[security] == 0:
        del Context.positions[security]

def order(security,amount):
    today_data = get_today_data(security)
    _order(today_data,security,amount)

def order_target(security,amount):
    if amount < 0:
        print("数量不能为负，已调整成0")
        amount = 0
    today_data = get_today_data(security)
    hold_amount = Context.positions.get(security,0)
    delta_amount = amount - hold_amount 
    _order(today_data,security,delta_amount)

def order_value(security,value):
    today_data = get_today_data(security)
    amount = int(value / today_data['开盘'])
    _order(today_data,security,amount)

def order_target_value(security,value):
    today_data = get_today_data(security)
    if value < 0:
        print('价值不能为负，已调整为0')
        value = 0 
    hold_value =  Context.positions.get(security,0) * today_data['开盘']
    delta_value = value - hold_value
    order_value(security,delta_value)

def run():
    plt_df = pd.DataFrame(index=pd.to_datetime(Context.date_range),columns=['value'])
    init_value = Context.cash
    initialize(Context)
    last_prize = {}
    for dt in Context.date_range:
        Context.dt = dateutil.parser.parse(dt)
        handle_data(Context)
        value = Context.cash 
        for stock in Context.positions:
            #考虑停牌的情况
            today_data  = get_today_data(stock)
            if len(today_data) == 0:
                p = float(last_prize[stock])
            else:
                p = float(today_data['开盘'])
                last_prize[stock] = p
            value += p * Context.positions[stock]
        plt_df.loc[dt,'value'] = value
    plt_df['ratio'] = (plt_df['value']-init_value)/init_value
    bm_df = attribute_daterange_history(Context.benchmark,Context.start_date,Context.end_date)
    bm_init = bm_df['开盘'][0]
    plt_df['benchmark_ratio'] = ((bm_df['开盘'] - bm_init)/bm_init).values
    plt_df[['ratio','benchmark_ratio']].plot()
    plt.show()
def initialize(Context):
    set_benchmark('601318') 
    g.p1 = 5 
    g.p2 = 60 
    g.security = '601318'
def handle_data(Context):
    hist = attribute_history(g.security,g.p2)
    ma5 = hist['收盘'][-g.p1:].mean()
    ma60 = hist['收盘'].mean()

    if ma5> ma60 and g.security not in Context.positions:
        order_value(g.security,Context.cash)
    elif ma5< ma60 and g.security in Context.positions:
        order_target(g.security,0)
        print('全部卖出')
run()
# t+1 手续费等