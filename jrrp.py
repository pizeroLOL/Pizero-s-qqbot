import GoCqhttpApi
import time
import random
import configparser

config = configparser.ConfigParser()
config.read('app-config.cfg',encoding='utf-8')

Function_topsecret = config['Function']
jrrp_type = Function_topsecret.getboolean('jrrp')


def jrrp(types, uid, gid):  # 今日人品
    if jrrp_type == True:
        timeis = time.strftime("%Y-%m-%d", time.localtime())  # 收到时间，格式为年-月-日
        config.read('jrrp.ini',encoding='utf-8')  # 读取jrrp.ini
        if config.has_section(timeis) == False:  # 判断文件中是否有时间相对应的表，没有则创捷
            config.add_section(timeis)
            with open('jrrp.ini', 'w',encoding='utf-8') as configfile:  # 写入jrrp.ini
                config.write(configfile)
        if config.has_option(timeis, str(uid)) == False:  # 有没有uid对应的项,没有就创建
            rp = random.randrange(0, 100, 1)  # 获得一个随机数
            config[timeis][str(uid)] = str(rp)  # 创建一个uid所对的项
            with open('jrrp.ini', 'w',encoding='utf8') as configfile:
                config.write(configfile)
        match types:
            case 'self':
                topsecret = config[timeis]  # 选中当前时间的表
                rp = topsecret[str(uid)]  # 发出将人品与表中uid相对
                rp = str(rp)
                if gid != None:
                    msg = '[CQ:at,qq='+uid+']你的人品为'+rp
                    GoCqhttpApi.sendmsg(msg, uid, gid)
                    if int(rp) < 20:
                        GoCqhttpApi.poke(uid, gid)
                else:
                    msg = '你的人品为'+rp
                    GoCqhttpApi.sendmsg(msg, uid)
            case 'others':
                topsecret = config[timeis]  # 选中当前时间的表
                rp = topsecret[str(uid)]  # 发出将人品与表中uid相对
                rp = str(rp)
                msg = str(uid)+'的人品为'+rp
                GoCqhttpApi.sendmsg(msg, uid, gid)
