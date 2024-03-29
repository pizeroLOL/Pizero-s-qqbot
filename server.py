from flask import Flask, request
from sqlalchemy import create_engine
import configparser
import GoCqhttpApi
import DataVisualization
import jrrp
import time
import os
import check
import pandas as pd

# 导入配置文件
config = configparser.ConfigParser()
config.read('app-config.cfg', encoding='utf-8')

# 检查
check.check()

# 参数导入
# uid表
id_topsecret = config['id']
Mascot_id = str(id_topsecret['Mascot_id'])
admin_id = str(id_topsecret['admin_id'])
robot_id = str(id_topsecret['robot_id'])
klt_id = str(id_topsecret['klt_id'])
look_for_group_id = str(id_topsecret['look_for_group_id'])
at_robot = '[CQ:at,qq='+robot_id+']'

# Function表
Function_topsecret = config['Function']
server_debug_type = Function_topsecret.getboolean('debug')
fuck_type = Function_topsecret.getboolean('fuck_type')
poke_type = Function_topsecret.getboolean('poke_type')
msglog_private_type = Function_topsecret.getboolean('msglog_private_type')
msglog_group_type = Function_topsecret.getboolean('msglog_group_type')

# main表
main_topsecret = config['main']
server_host = main_topsecret['host']
server_post = main_topsecret["port"]

# 导入QAs
QAs = pd.read_csv('./QAs.csv', encoding='utf8')
QAs_list = list(QAs['Q'])

for Q in QAs_list:
    Q_all = '%0A' + Q

# 删除多余变量
del id_topsecret, Function_topsecret, main_topsecret

# 其他全局变量
diff_time = None
msg_step = 0
gid = None
engine = create_engine('sqlite:///bot.db')


def keyword(message, uid, gid=None):
    '''中转，将各个的应用转到对应的模块'''
    # 初始化
    global diff_time, msg_step
    uid = str(uid)
    if gid != None:
        gid = str(gid)
    # 转发至模块
    message = message
    solve_list = [at_robot, to_jrrp,
                  songs, Q_rp, eggs, pokepoke, DV, QAs_Q, find_msg]
    for func in solve_list:
        func(message, uid, gid)
    # 发言频率检测
    # if time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) != diff_time :
    #     diff_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     msg_step = msg_step + 1
    # else:
    #     msg_step = 0
    # if msg_step == 2:
    #     return tell_admin(admin_id,uid,gid)


# def helps(message: str, uid: str | int, gid=None):
#     '''帮助'''
#     if message == '#help' or message == '#帮助' or message == '#幫助' or message == '#使用說明':
#         next_len = '%0A'
#         msgs = ['输入%23help来获取本帮助'+next_len+'@QQ 机器人来通过戳一戳（双击头像的那种）来确认是否在线', '输入（jrrp）或者（今日人品）来获得今天的“人品”'+next_len+'输入（%23人品查询（空格）<查询uid>）来获取某人的“人品”', '输入（%23点歌）或者（%23點歌）来通过输入songid点歌'+next_len + '使用案例'+next_len +
#                 '    %23点歌（空格）<QQ音乐/网易云音乐/qqyy/qq/wyyyy/wy>（空格）<歌曲id，怎么获取自己查>', '输入（晚安）时，机器人会返回一句晚安'+next_len + '输入（%23戳一戳）来让机器人双击不方便戳的人', '输入（Q:【问题】）获取在文档内的问腿'+next_len+'输入(%23全部问题)获取在文档内的全部问题']
#         for msg in msgs:
#             GoCqhttpApi.sendmsg(msg, uid, gid)
#             time.sleep(1)
#         if fuck_type == True:
#             msg = '输入（可乐兔三联）来让可乐兔再次快乐'
#             GoCqhttpApi.sendmsg(msg, uid, gid)
#         if poke_type == True:
#             msg = '输入（摸摸吉祥物）让吉祥物再次快乐'
#             GoCqhttpApi.sendmsg(msg, uid, gid)
#         if msglog_group_type == True or msglog_private_type == True:
#             msg = '输入（%23top20）获取当月发消息榜单top20。%0A输入（%23月发信息表）获取当月发消息的数量与人数的表。输入（%23活跃时间）获取活跃的时间与小时关系表。输入（#活跃时间散点）获取活跃时间散点'
#             GoCqhttpApi.sendmsg(msg, uid, gid)


def at_robot(message, uid, gid):
    '''机器人在线检测'''
    if message == at_robot:
        return GoCqhttpApi.poke(uid, gid)


def to_jrrp(message, uid, gid):
    '''今日人品'''
    if message[0:4] == '今日人品' or message[0:4] == 'jrrp':
        types = 'self'
        return jrrp.jrrp(types, uid, gid)


def songs(message, uid, gid):
    '''点歌'''
    if message[0:3] == '#点歌' or message[0:3] == '#點歌':
        message = message[4:]
        return GoCqhttpApi.songs(message, uid, gid)


def Q_rp(message, uid, gid=None):
    '''人品查询'''
    if message[0:5] == '#人品查询' or message[0:5] == '#rpcx' or message[0:5] == '#人品査詢':
        if len(message) > 8:
            uid = message[6:]
            types = 'others'
        else:
            types = 'self'
        return jrrp.jrrp(types, uid, gid)


def eggs(message, uid, gid):
    '''彩蛋'''
    if message[0:5] == '摸摸吉祥物' and poke_type == True:
        uid = Mascot_id
        return GoCqhttpApi.poke(uid, gid)
    elif message[0:5] == '可乐兔三连' or message[0:5] == '可樂兔三連' and fuck_type == True:
        msgs = ['可乐兔整合包更了吗', '可乐兔模组更了吗', '提学分了吗']
        for msg in msgs:
            GoCqhttpApi.sendmsg(msg, uid, gid)
            time.sleep(1)


def pokepoke(message, uid, gid):
    '''戳人'''
    if message[0: 5] == '#poke' or message[0:2] == '#戳' or message[0:4] == '#戳一戳':
        print(message+uid)
        if len(message) > 8:
            return others_poke(message, uid, gid)
        else:
            message = '#poke '+str(uid)
            return others_poke(message, uid, gid)


def DV(message, uid, gid):
    '''调用写好的数据可视化'''
    types = 'private'
    tf = True
    if gid != None:
        types = 'gourp'
    if (types == 'private' and msglog_private_type != True) or (types == 'group' and msglog_group_type != True):
        tf = False
    if tf == True:
        match message:
            case '#top20':
                return DataVisualization.monthly_sendmsg_top20(uid, gid)
            case '#月发信息表':
                return DataVisualization.nmsm(uid, gid)
            case '#活跃时间':
                return DataVisualization.sinehtm(uid, gid)
            case '#活跃时间散点图':
                return DataVisualization.atsm(uid, gid)


def QAs_Q(message, uid, gid=None):
    '''自定义QAs'''
    if message[:2] == 'Q:' or message[:2] == 'Q：' and QAs['Q'].str.contains(message[2:]) == True:
        date = QAs.loc[QAs['Q'].str.contains(message[2:])]
        msg = date.iloc[0, 1]
        GoCqhttpApi.sendmsg(msg, uid, gid)
    elif message[:5] == '#全部问题':
        GoCqhttpApi.sendmsg(Q_all, uid, gid)


def find_msg(message, uid, gid=None):
    '''消息查询'''
    if message[:5] == '#消息查询':
        finder = message[6:]
        finding_msg(finder, uid, gid)
    if message[:6] == '#fdmsg':
        finder = message[7:]
        finding_msg(finder, uid, gid)


def finding_msg(finder, uid, gid=None):
    uid = str(uid)
    finder = str(finder)
    if gid != None:
        prefix = 'gid-'+gid
    else:
        prefix = 'uid-'+uid
    try:
        msgs = pd.read_sql(prefix, engine)
    except FileNotFoundError as err:
        GoCqhttpApi.sendmsg('无记录或未开启消息记录', uid, gid)
    # print(msgs)
    # print(msgs['message'])
    tf_list = list(msgs.message.str.contains(finder))
    if True in tf_list:
        tf = True
    else:
        tf = False
    if tf == True:
        df = msgs.loc[msgs['message'].str.contains(finder, na=False)]
        msglist = list(df['message'])
        msg = '结果如下'
        for i in msglist:
            msg = msg + '%0A' + i
        GoCqhttpApi.sendmsg(msg, uid, gid)
    else:
        GoCqhttpApi.sendmsg('无符合条件的消息', uid, gid)


def others_poke(message, uid, gid):
    if message[0: 5] == '#poke':
        uid = message[6:]
    elif message[0:2] == '#戳':
        uid = message[3:]
    elif message[0:4] == '#戳一戳':
        uid = message[5:]
    GoCqhttpApi.poke(uid, gid)


def tell_admin(admin_id, uid, gid):
    msg = '[CQ:at,qq='+admin_id+'] 每秒发送超过3条信息，关注一下'
    GoCqhttpApi.sendmsg(msg, uid, gid)

# def send_top(uid,gid = None):
#     if gid == None:


'''记录信息发送'''


def group(msg, uid, gid):
    if msglog_group_type == True:
        gid = str(gid)
        timeis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        df = pd.DataFrame({
            'message': [msg],
            'time': [timeis],
            'uid': [uid],
            'gid': [gid]
        })
        df.to_sql('gid-'+gid, engine, if_exists='append', index=False)


def private(msg, uid):
    if msglog_private_type == True:
        uid = str(uid)
        timeis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # columns = ['msg','uid','gid']
        df = pd.DataFrame({
            'message': [msg],
            'time': [timeis],
            'uid': [uid]
        })
        df.to_sql('uid-'+uid, engine, if_exists='append', index=False)


# 服务端本体
app = Flask(__name__)


@app.route("/", methods=["POST"])
def return_app():
    # 下面的request.get_json().get......是用来获取关键字的值用的，关键字参考上面代码段的数据格式
    if request.get_json().get('message_type') == 'private':  # 如果是私聊信息
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        private(message, uid)
        keyword(message, uid)  # 将 Q号和原始信息传到我们的后台
    if request.get_json().get('message_type') == 'group':  # 如果是群聊信息
        gid = request.get_json().get('group_id')  # 获取群号
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        group(message, uid, gid)
        keyword(message, uid, gid)  # 将 Q号和原始信息传到我们的后台
    return 'OK'


if __name__ == '__main__':
    app.run(debug=server_debug_type, host=server_host, port=server_post)
