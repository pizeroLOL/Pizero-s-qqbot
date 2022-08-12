import GoCqhttpApi
import time
import random
import configparser
import sqlalchemy
import pandas as pd

config = configparser.ConfigParser()
config.read('app-config.cfg', encoding='utf-8')

Function_topsecret = config['Function']
jrrp_type = Function_topsecret.getboolean('jrrp')

engine = sqlalchemy.create_engine('sqlite:///bot.db')


def new_rp(uid):
    '''新的当日人品'''
    timeis = time.strftime("%Y-%m-%d", time.localtime())
    rp = random.randrange(0, 100, 1)  # 获得一个随机数
    df = pd.DataFrame([{
        'date': timeis,
        'id': uid,
        'rp': rp,
    }])
    df.to_sql('jrrp', engine, if_exists='append', index=False)
    return rp


def Q_jrrp(uid):
    """查询今日人品"""
    '''获取时间，格式为年-月-日'''
    timeis = time.strftime("%Y-%m-%d", time.localtime())
    '''读取sql的今日人品, 如果没有数据库文件就新建'''
    try:
        df = pd.read_sql('jrrp', engine)
    except sqlalchemy.exc.OperationalError:
        return new_rp(uid)
    '''检测是否有当日的人品'''
    if timeis not in df['date'].values:
        return new_rp(uid)
    today_df = df.loc[df['date'].str.contains(timeis)]
    '''检测当日人品是否有当前uid'''
    if uid not in today_df['id'].values:
        return new_rp(uid)
    today_df = today_df.set_index('id')
    return today_df.loc[uid, 'rp']


def jrrp(types, uid, gid=None):
    '''今日人品'''
    if jrrp_type == True:
        rp = str(Q_jrrp(uid))
        match types:
            case 'self':
                msg = '你的人品为'+rp
                if gid != None or gid != 'None':
                    msg = '[CQ:at,qq='+uid+']你的人品为'+rp
                GoCqhttpApi.sendmsg(msg, uid, gid)
            case 'others':
                msg = str(uid)+'的人品为'+rp
                GoCqhttpApi.sendmsg(msg, uid, gid)
