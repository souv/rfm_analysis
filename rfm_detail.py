import os
import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import dtale

host = "xxx"
dbname = "yyy"
user = "zzz"
password = "www"

conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, password)
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
cursor.execute("")

data = pd.DataFrame(cursor.fetchall())
column_names = [i[0] for i in cursor.description]
data.columns = column_names
print(data.info())

#rfm binning
r_label = ['R(0-25)','R(25-50)','R(50-75)','R(75-100)']
data['r_label'] = pd.qcut(data['last_buy_interval'], q=4,labels = r_label)

f_label = ['F(1 time)','F(2-5 times)','F(6-10 times)','F(10 times above)']
cut_bins = [0,1,5,10,1000]
data['f_label'] = pd.cut(data['frequency'],bins = cut_bins,labels = f_label)

m_label = ['M(0-25)','M(25-50)','M(50-75)','M(75-100)']
data['m_label'] = pd.qcut(data['sum_monetary_value'], q=4,labels = m_label)

#看各變數的分布狀況
print(data[['r_label','last_buy_interval']].groupby('r_label').mean())

print(data[['f_label','frequency']].groupby('f_label').mean())

print(data[['m_label','sum_monetary_value']].groupby('m_label').mean())

#用一行程式碼做描述性統計
d = dtale.show(data)
d.open_browser()

#make the rfm table
rfm_pivot_table = data[['r_label','f_label','m_label','sum_monetary_value']].groupby(['r_label', 'f_label', 'm_label']).agg(['count','sum','mean']).reset_index()

rfm_pivot_table.to_excel('rfm_pivot_table2.xlsx',encoding ='utf_8_sig')
