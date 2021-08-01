import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak 
df = pd.read_csv('600031.csv',index_col="日期",parse_dates=['日期'])[['开盘','收盘','最高','最低','涨跌幅']]
#五日均线 30日均线
# df['ma5'] = np.nan
# df['ma30'] = np.nan

# for i in range(4,len(df)):
#     df.loc[df.index[i],'ma5'] = df['收盘'][i-4:i+1].mean()
# for i in range(29,len(df)):
#     df.loc[df.index[i],'ma30'] = df['收盘'][i-29:i+1].mean()
# print(df)
df['ma5'] = df['收盘'].rolling(5).mean()
df['ma30'] = df['收盘'].rolling(30).mean()
# df = df[-200:]
# df[['收盘','ma5','ma30']].plot()
# plt.show()
df = df.dropna()
# golden_cross = []
# death_cross = []
# for i in range(1,len(df)):
#     if df['ma5'][i] >= df['ma30'][i] and df['ma5'][i-1] < df['ma30'][i-1]:
#         golden_cross.append(df.index[i])
#     if df['ma5'][i] <= df['ma30'][i] and df['ma5'][i-1] > df['ma30'][i-1]:
#         death_cross.append(df.index[i])
# print(death_cross) 
sr1 = df['ma5'] < df['ma30']
sr2 = df['ma5'] > df['ma30']

death_cross = df[sr1 & sr2.shift(1)].index
golden_cross = df[~(sr1 | sr2.shift(1))].index
print(golden_cross)