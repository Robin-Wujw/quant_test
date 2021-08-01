import akshare as ak 
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 

df  = pd.read_csv("600031.csv",index_col="日期",parse_dates=['日期'])[['开盘','收盘','最高','最低','涨跌幅']]
#涨跌幅大于3%
#print(df[df['涨跌幅']>3].index)
#开盘比前日收盘跌幅超过2%
# print(df[df['开盘']-df['收盘'].shift(1)/df['收盘'].shift(1)>=10].index)
# print(df[(df['开盘']-df['收盘'].shift(1))/df['收盘'].shift(1)<=-0.02].index)
# for i in range(1,len(df)):
#     if (df.iloc[i,0]-df.iloc[i-1,1])/df.iloc[i-1,1] <=-0.02:
#          print(df.iloc[i].name.date())
#假如我从2010年1月1日开始,每月第一个交易日买入1手股票，每年最后一个交易日卖出所有股票，到今天为止，我的收益如何
price_last = df['开盘'][-1]
df_monthly = df.resample('M').first()
df_yearly = df.resample('A').last()[:-1]
cost_money = 0
hold = 0
for year in range(2015,2022):
    cost_money += df_monthly.loc[str(year)]['开盘'].sum()*100
    hold +=len(df_monthly.loc[str(year)]['开盘']) *100
    if year!=2021:
        cost_money -= df_yearly.loc[str(year)]['开盘'][0]*hold
        hold = 0
cost_money -= hold*price_last
print(-cost_money)
# print(df_monthly['2015'])