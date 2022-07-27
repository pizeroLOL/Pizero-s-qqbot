from flask import Flask, request
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
config.read('app-config.cfg')

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
    Q_all = Q + '\n'

# 删除多余变量
del id_topsecret, Function_topsecret, main_topsecret

# 其他全局变量
diff_time = None
msg_step = 0
gid = None


def keyword(message, uid, gid=None):
    '''中转，将各个的应用转到对应的模块'''
    # 初始化
    global diff_time, msg_step
    uid = str(uid)
    if gid != None:
        gid = str(gid)
    # 转发至模块
    message = message
    solve_list = [helps, at_robot, to_jrrp, songs, Q_rp, eggs, pokepoke,DV, QAs_Q]
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


def helps(message:str, uid:str|int, gid=None):
    '''帮助'''
    if message[0:5] == '#help' or message[0:3] == '#帮助' or message[0:3] == '#幫助' or message[0:5] == '' or message[0:5] == '#使用說明':
        next_len = '%0A'
        msgs = ['输入%23help来获取本帮助'+next_len+'@QQ 机器人来通过戳一戳（双击头像的那种）来确认是否在线'+next_len+'输入（jrrp）或者（今日人品）来获得今天的“人品”'+next_len+'输入（%23点歌）或者（%23點歌）来通过输入songid点歌', '使用案例'+next_len +
                '    %23点歌（空格）<QQ音乐/网易云音乐/qqyy/qq/wyyyy/wy>（空格）<歌曲id，怎么获取自己查>', '输入（晚安）时，机器人会返回一句晚安'+next_len + '输入（%23人品查询（空格）<查询uid>）来获取某人的“人品”'+next_len + '输入（%23戳一戳）来让机器人双击不方便戳的人']
        for msg in msgs:
            GoCqhttpApi.sendmsg(msg, uid, gid)
            time.sleep(1)
        if fuck_type == True:
            klt_yes = '输入（可乐兔三联）来让可乐兔再次快乐'
            GoCqhttpApi.sendmsg(klt_yes, uid, gid)
        if poke_type == True:
            poke_yes = '输入（摸摸吉祥物）让吉祥物再次快乐'
            GoCqhttpApi.sendmsg(poke_yes, uid, gid)


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
        return others_poke(message, uid, gid)


def DV(message,uid,gid):
    '''调用写好的数据可视化'''
    match message:
        case '#top20':
            return DataVisualization.monthly_sendmsg_top20(uid,gid)
        case '#月发信息表':
            return DataVisualization.nmsm(uid, gid)
        case '#活跃时间':
            return DataVisualization.sinehtm(uid, gid)
        case '#活跃时间散点':
            return DataVisualization.atsm(uid, gid)


def QAs_Q(message, uid, gid=None):
    '''自定义QAs'''
    if message[:2] == 'Q:' or message[:2] == 'Q：' and QAs['Q'].str.contains(message[2:]) == True:
        print(QAs)
        date = QAs.loc[QAs['Q'].str.contains(message[2:])]
        print(date)
        msg = date.iloc[0, 1]
        print(msg)
        GoCqhttpApi.sendmsg(msg, uid, gid)
    elif message[:5] == '#全部问题':
        GoCqhttpApi.sendmsg(Q_all, uid, gid)

# def QQ(message,uid,gid):
#     if message == '?':
#         GoCqhttpApi.sendmsg('?',uid,gid)

# 应用模块例子
# def xxxxx(xxx,xxx,xxx):
    # msg=''
    # sendmsg(msg,uid,gid)

# msg为发送的信息
# uid为发送者
# gid为收到消息的群


def others_poke(message, uid, gid):
    if message[0: 5] == '#poke':
        uid = message[5:]
    elif message[0:2] == '#戳':
        uid = message[3:]
    elif message[0:4] == '#戳一戳':
        uid = message[4:]
    GoCqhttpApi.poke(uid, gid)


def tell_admin(admin_id, uid, gid):
    msg = '[CQ:at,qq='+admin_id+'] 每秒发送超过3条信息，关注一下'
    GoCqhttpApi.sendmsg(msg, uid, gid)

# def sand_top(uid,gid = None):
#     if gid == None:


'''记录信息发送'''


def group(msg, uid, gid):
    if msglog_group_type == True:
        gid = str(gid)
        timeis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file_path = './msglog/'+'gid-'+gid+'/' + \
            time.strftime("%Y-%m", time.localtime())+'.csv'
        tmpfm = pd.DataFrame({
            'message': [msg],
            'time': [timeis],
            'uid': [uid],
            'gid': [gid]
        })
        if os.path.exists('./msglog/gid-'+gid) == False:
            os.makedirs('msglog/gid-'+gid)
        if os.path.isfile(file_path) == True:
            tmpfm.to_csv(file_path, index=None, header=False, mode='a')
        elif os.path.isfile(file_path) == False:
            tmpfm.to_csv(file_path, index=None, mode='w')


def private(msg, uid):
    if msglog_private_type == True:
        uid = str(uid)
        timeis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # columns = ['msg','uid','gid']
        file_path = './msglog/uid-'+uid+'/' + \
            time.strftime("%Y-%m", time.localtime())+'.csv'
        tmpfm = pd.DataFrame({
            'message': [msg],
            'time': [timeis],
            'uid': [uid]
        })
        if os.path.exists('./msglog/uid-'+uid) == False:
            os.makedirs('msglog/uid-'+uid)
        if os.path.isfile(file_path) == True:
            tmpfm.to_csv(file_path, index=None, header=False, mode='a')
        elif os.path.isfile(file_path) == False:
            tmpfm.to_csv(file_path, index=None, mode='w')


# 服务端本体
app = Flask(__name__)


@app.route("/", methods=["POST"])
def return_app():
    # 下面的request.get_json().get......是用来获取关键字的值用的，关键字参考上面代码段的数据格式
    if request.get_json().get('message_type') == 'private':  # 如果是私聊信息
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        keyword(message, uid)  # 将 Q号和原始信息传到我们的后台
        private(message, uid)
    if request.get_json().get('message_type') == 'group':  # 如果是群聊信息
        gid = request.get_json().get('group_id')  # 获取群号
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        keyword(message, uid, gid)  # 将 Q号和原始信息传到我们的后台
        group(message, uid, gid)
    return 'OK'


if __name__ == '__main__':
    app.run(debug=server_debug_type, host=server_host, port=server_post)
