
'''
编写参考 
https://www.cnblogs.com/xiaoshun-mjj/p/14516964.html
https://blog.csdn.net/liuyingying0418/article/details/100126348
'''
from time import sleep
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# 常用参数导入
# csv_path = sys.argv[1]

# 正常显示中文和负号
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 画图的样式风格设置为：ggplot
plt.style.use('ggplot')

# 读取 csv
# df = pd.read_csv(csv_path)
with open('D:/编写中/cqhttp/apps/msglog/gid-1004741240/2022-07.csv', 'r', encoding='utf-8') as csv:
    df = pd.read_csv(csv)

"""时间格式转换"""
# 获取时间
df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
# 月

'''消息发送top 排名'''
uid_step = df['uid'].value_counts()
uid_step.columns = ['左uid，右次数']
uid_top = uid_step.reset_index()
uid_top.index = range(len(uid_top))
uid_top.index=uid_top.index+1
uid_top.columns = ['uid','次数']
print('单位时间发送消息top20')
print(uid_top.head(20))

'''单位时间发送消息分布'''
plt.figure(figsize=(5, 3))
plt.subplot(1, 1, 1)
uid_step.plot.hist(bins=30, title='发送消息分布')
plt.savefig('发送消息分布')

'''活跃时间散点图'''
df['hour'] = df['time'].dt.hour
df['minute'] = df['time'].dt.minute
df['second'] = df['time'].dt.second
df['float_hours'] = df['hour'] + df['minute']/60
msg_presecend = df['float_hours'].value_counts()
msg_presecend = msg_presecend.reset_index()
msg_presecend.columns = ['时间-小时与分钟', '消息数']
msg_presecend.plot.scatter(x='消息数', y='时间-小时与分钟')
plt.savefig('活跃时间散点图')
# print(msg_presecend)
# plt.show()

'''每小时在线分布'''
msg_prehours = df['hour'].value_counts()
msg_prehours = msg_prehours.reset_index()
msg_prehours.columns = ['小时', '消息数']
msg_prehours = msg_prehours.sort_values(by = ['小时', '消息数'])
msg_prehours = msg_prehours.reset_index(drop=True)
msg_prehours.plot(x='小时', y='消息数')
plt.savefig('每小时在线分布')
# print(msg_prehours)
# plt.show()

# '''最晚消息'''
# lastest_msg=df
# lastest_msg.index=df['hour']
# hour_tmp = lastest_msg.query('hour == 4 and minute < 30')
# if len(hour_tmp) > 0 :
#     lastest_msg.index=df['minute']

# print(hour_tmp)