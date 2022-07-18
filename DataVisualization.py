
'''
编写参考 
https://www.cnblogs.com/xiaoshun-mjj/p/14516964.html
https://blog.csdn.net/liuyingying0418/article/details/100126348
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# 常用参数导入
csv_path = sys.argv[1]

# 正常显示中文和负号
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 画图的样式风格设置为：ggplot
plt.style.use('ggplot')

# 读取 csv
df = pd.read_csv(csv_path)

"""时间格式转换"""
# 获取时间
df['timeis'] = pd.to_datetime(df['timeis'],format='%Y-%m-%d %H:%M:%S')
# 月
df['month'] = df['timeis'].values.astype('datatime64[M]')
print(df)