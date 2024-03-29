
'''
编写参考
https://www.cnblogs.com/xiaoshun-mjj/p/14516964.html
https://blog.csdn.net/liuyingying0418/article/details/100126348
'''
import platform
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import time
import GoCqhttpApi
from sqlalchemy import create_engine


# 正常显示中文和负号
plt.rcParams['font.sans-serif'] = ['MiSans', 'HeiTi', 'KaiTi', 'SimHei', 'Song', 'Fangsong',
                                   'Ubuntu Mono', 'NotoSans', 'Noto Sans CJK SC', 'Microsoft Yahei', 'Heiti SC Medium']
plt.rcParams['axes.unicode_minus'] = False
# 画图的样式风格设置为：ggplot
plt.style.use('ggplot')

# 设置数据库地址
engine = create_engine('sqlite:///bot.db')


class PermissionError(BaseException):
    '''你他喵要么每天好地址，要么没填好gid'''
    ...


def read_sqlite_db(uid: str | int, gid: str | int, types: str):
    '''读取 sqlite database'''
    global df, uid_step
    table = 'gid-' + str(gid)
    if gid == None or gid == 'None':
        table = 'uid-' + str(uid)
    df = pd.read_sql(table, engine)
    """时间格式转换"""
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    # print(df)
    return table_conversion(types)


def table_conversion(types: str):
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month
    df['hour'] = df['time'].dt.hour
    df['minute'] = df['time'].dt.minute
    df['second'] = df['time'].dt.second
    df['float_hours'] = df['hour'] + df['minute']/60
    match types:
        case 'uid_step' | 'uid_top':
            mid_tmp = df.query('year == {0} and month == {1}'.format(time.strftime("%Y", time.localtime()),
                time.strftime("%m", time.localtime())))
            uid_step = mid_tmp['uid'].value_counts()
            uid_step.columns = ['左uidX，右次数']
            if types == 'uid_top':
                uid_top = uid_step.reset_index()
                uid_top.index = range(len(uid_top))
                uid_top.index = uid_top.index+1
                uid_top.columns = ['uid', '次数']
                return uid_top
            return uid_step
        case 'msg_presecend':
            msg_presecend = df['float_hours'].value_counts()
            msg_presecend = msg_presecend.reset_index()
            msg_presecend.columns = ['时间-小时与分钟', '消息数']
            return msg_presecend
        case 'msg_prehours':
            msg_prehours = df['hour'].value_counts()
            msg_prehours = msg_prehours.reset_index()
            msg_prehours.columns = ['小时', '消息数']
            msg_prehours = msg_prehours.sort_values(by=['小时', '消息数'])
            msg_prehours = msg_prehours.reset_index(drop=True)
            return msg_prehours


def monthly_sendmsg_top20(uid: str | int, gid: str | int):
    '''消息发送top20'''
    uid_top = read_sqlite_db(uid, gid, 'uid_top')
    # try:
    tmp_fm = uid_top.head(20)
    tmp_fm2list_1 = list(tmp_fm['uid'])
    tmp_fm2list_2 = list(tmp_fm['次数'])
    msg = '本月消息发送top20%0A QQ号        uid%0A'
    if len(tmp_fm2list_1) != len(tmp_fm2list_2):
        print('长度不符，请检查代码')
        GoCqhttpApi.sendmsg('长度不符，请检查代码', str(uid), str(gid))
    for x in range(len(tmp_fm2list_1)):
        msg = msg + '%0A' + \
            str(tmp_fm2list_1[x]) + '  ' + str(tmp_fm2list_2[x])
    GoCqhttpApi.sendmsg(msg, str(uid), str(gid))
    # except AttributeError as e:
    #     GoCqhttpApi.sendmsg('请检查msglog是否开启，如果没有，那么正常',uid,gid)
    # print(msg)


def nmsm(uid: str | int, gid: str | int):
    '''当月单位消息数发送成员数'''
    return the_number_of_units_in_the_month_of_the_month_sent_the_number_of_members(uid, gid)


def the_number_of_units_in_the_month_of_the_month_sent_the_number_of_members(uid: str | int, gid: str | int):
    '''当月单位消息数发送成员数'''
    uid_step = read_sqlite_db(uid, gid, 'uid_step')
    # try:
    plt.figure(figsize=(5, 3))
    plt.subplot(1, 1, 1)
    uid_step.plot.hist(bins=30, title='发送消息分布')
    plt.savefig('发送消息分布')
    prefix = 'file:///'
    if platform.system() != 'Windows':
        prefix = 'file://'
    paths = prefix + \
        os.path.split(os.path.realpath(sys.argv[0]))[0] + '\发送消息分布.png'
    # print(paths)
    plt.close()
    GoCqhttpApi.image(uid, gid, paths)
    # except AttributeError as e:
    #     GoCqhttpApi.sendmsg('请检查msglog是否正常或是否开启')


def atsm(uid: str | int, gid: str | int):
    '''活跃时间散点图'''
    return active_time_scatter_map(uid, gid)


def active_time_scatter_map(uid: str | int, gid: str | int):
    '''活跃时间散点图'''
    msg_presecend = read_sqlite_db(uid, gid, 'msg_presecend')
    msg_presecend.plot.scatter(x='消息数', y='时间-小时与分钟')
    plt.savefig('活跃时间散点图')
    prefix = 'file:///'
    if platform.system() != 'Windows':
        prefix = 'file://'
    paths = prefix + \
        os.path.split(os.path.realpath(sys.argv[0]))[0] + '\活跃时间散点图.png'
    # print(paths)
    plt.close()
    GoCqhttpApi.image(uid, gid, paths)
    # plt.show()`


def sinehtm(uid: str | int, gid: str | int):
    return send_information_number_every_hour_that_month(uid, gid)


def send_information_number_every_hour_that_month(uid: str | int, gid: str | int):
    '''当月每小时发送信息条数折线图'''
    msg_prehours = read_sqlite_db(uid, gid, 'msg_prehours')
    # print(msg_prehours)
    msg_prehours.plot(x='小时', y='消息数')
    plt.savefig('每小时在线分布')
    prefix = 'file:///'
    if platform.system() != 'Windows':
        prefix = 'file://'
    paths = prefix + \
        os.path.split(os.path.realpath(sys.argv[0]))[0] + '\每小时在线分布.png'
    # print(paths)
    plt.close()
    GoCqhttpApi.image(uid, gid, paths)
    # plt.show()

# '''最晚消息'''
# lastest_msg=df
# lastest_msg.index=df['hour']
# hour_tmp = lastest_msg.query('hour == 4 and minute < 30')
# if len(hour_tmp) > 0 :
#     lastest_msg.index=df['minute']

# print(hour_tmp)
