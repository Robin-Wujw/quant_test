import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import akshare as ak
import dateutil
import datetime

CASH = 100000
START_DATE = '2019-01-01'
END_DATE = '2021-8-17'
trade_cal = pd.read_csv('trade_date.csv')
class Context:
    def __init__(self,cash,start_date,end_date):
        self.cash = cash 
        self.start_date = start_date
        self.end_date = end_date 
        self.positions = {}
        self.benchmark = None 
        self.date_range = trade_cal[(trade_cal['trade_date']>=start_date)& (trade_cal['trade_date']<=end_date)]['trade_date'].values
        self.dt = dateutil.parser.parse(start_date)
class G:
    pass
g = G()
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

print(attribute_history('600031',20))