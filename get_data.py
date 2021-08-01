import akshare as ak
data_31 = ak.stock_zh_a_hist(symbol="600031", start_date="20150301", end_date='20210731', adjust="qfq")
data_31.to_csv('600031.csv')