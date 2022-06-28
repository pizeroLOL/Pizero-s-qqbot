import GoCqhttpApi
import jrrp
import time
import configparser

config = configparser.ConfigParser()
config.read('app-config.cfg')

# 参数导入
## uid表
uid_topsecret = config['uid']
Mascot_id = str(uid_topsecret['Mascot_id'])
admin_id = str(uid_topsecret['admin_id'])
robot_id = str(uid_topsecret['robot_id'])
at_robot = '[CQ:at,qq='+robot_id+']'

## klt表
klt_topsecret = config['klt']
klt_id = str(klt_topsecret['uid'])
fuck_type = klt_topsecret.getboolean('fuck_type')

# 吉祥物表
Mascot_topsecret = config['Mascot']
poke_type = Mascot_topsecret.getboolean('poke_type')

def keyword(message,uid,gid = None):
    uid=str(uid)
    if gid != None:
        gid=str(gid)
    if message[0:5] == '#help' or message[0:3] == '#帮助' or message[0:3] == '#幫助' or message[0:5] == '' or message[0:5] == '#使用說明':
        return helps(uid,gid)

    elif message[0:21] == at_robot :
        return GoCqhttpApi.poke(uid,gid)

    elif message[0:4] == '今日人品' or message[0:4]=='jrrp':
        types='self'
        return jrrp.jrrp(types,uid,gid)

    elif message[0:3] == '#点歌' or message[0:3] == '#點歌':
        message = message[4:]
        return GoCqhttpApi.songs(message,uid,gid)

    elif message[0:2] == '晚安':
        return good_night(uid,gid)

    elif message[0:5] == '#人品查询' or message[0:5] == '#rpcx' or message[0:5] == '#人品査詢':
        if len(message) > 8 :
            uid = message[6:]
            types='others'
        else:
            types='self'
        return jrrp.jrrp(types,uid,gid)

    elif message[0:5] == '摸摸吉祥物':
        if poke_type == True:
            uid = Mascot_id
            return GoCqhttpApi.poke(uid,gid)
    elif message[0:5] == '可乐兔三连' or message[0:5] == '可樂兔三連':
        if fuck_type == True:
            msgs=['可乐兔整合包更了吗','可乐兔模组更了吗','提学分了吗']
            for msg in msgs:
                GoCqhttpApi.sendmsg(msg,uid,gid)
                time.sleep(1)
        
    elif message[0: 5] == '#poke' or message[0:2] == '#戳' or message[0:4] == '#戳一戳' :
        return others_poke(message,uid,gid)

### 屏蔽词相关
    # elif message[0:7] == '!addpbc':
    #     pbc = message[8:]
    #     return addpbc(pbc,uid,gid)
    # elif message[0:6] == '！添加屏蔽词':
    #     pbc = message[7:]
    #     return addpbc(pbc,uid,gid)
    # elif message[0:6] == '!dlpbc' or message[0:6] == '！删除屏蔽词':
    #     pbc = message[7:]
    #     return dlpbc(pbc,uid,gid)

    # elif message[0:9] == '!addadmin':
    #     doadmin = 'admin'+str(gid)+str(message[10:])
    #     return addadmin(doadmin,uid,gid)
    # elif message[0:6] == '！添加管理员':
    #     doadmin = 'admin'+str(gid)+str(message[7:])
    #     return addadmin(doadmin,uid,gid)

    # elif message[0:8] == '!dladmin':
    #     doadmin = 'admin'+str(gid)+str(message[9:])
    #     #return dladmin(doadmin,uid,gid)


## 应用模块例子
#def xxxxx(xxx,xxx,xxx):  
    #msg=''
    #sendmsg(msg,uid,gid)

## msg为发送的信息
## uid为发送者
## gid为收到消息的群

def helps(uid,gid = None): #帮助
    next_len = '%0A'
    msgs=['输入%23help来获取本帮助'+next_len+'@QQ 机器人来通过戳一戳（双击头像的那种）来确认是否在线'+next_len+'输入（jrrp）或者（今日人品）来获得今天的“人品”'+next_len+'输入（%23点歌）或者（%23點歌）来通过输入songid点歌','使用案例'+next_len + '    %23点歌（空格）<QQ音乐/网易云音乐/qqyy/qq/wyyyy/wy>（空格）<歌曲id，怎么获取自己查>','输入（晚安）时，机器人会返回一句晚安'+next_len + '输入（%23人品查询（空格）<查询uid>）来获取某人的“人品”'+next_len + '输入（%23戳一戳）来让机器人双击不方便戳的人']
    for msg in msgs:
        GoCqhttpApi.sendmsg(msg,uid,gid)
        time.sleep(1)
    if fuck_type == True:
        klt_yes = '输入（可乐兔三联）来让可乐兔再次快乐'
        GoCqhttpApi.sendmsg(klt_yes,uid,gid)
    if poke_type == True:
        poke_yes = '输入（摸摸吉祥物）让吉祥物再次快乐'
        GoCqhttpApi.sendmsg(poke_yes,uid,gid)

def good_night(uid,gid = None):  
    msg='晚安'
    GoCqhttpApi.sendmsg(msg,uid,gid)

def others_poke(message,uid,gid):
    if message[0: 5] == '#poke' :
        uid = message[5:]
    elif message[0:2] == '#戳' :
        uid = message[3:]
    elif message[0:4] == '#戳一戳' :
        uid = message[4:]
    GoCqhttpApi.poke(uid,gid)

### 屏蔽词相关
# def addpbc(pbc,uid,gid):
#     doadmin = 'admin'+str(gid)+str(uid)
#     config.read('pbc.ini')
#     if str(uid) == admin or config.has_option(str(gid),doadmin) == True :
#         if gid != None:
#             if pbc == '!addpbc' or pbc == '!dlpbc' or pbc == '！添加屏蔽词' or '！删除屏蔽词' or pbc== 'admin':
#                 msg='你想写出bug直说，我来给你写'
#                 sendmsg(msg,gid)
#             else:
#                 if config.has_section(str(gid)) == False:
#                     config[str(gid)]={'12154152151221111684215231521511111':'0'}
#                     with open('pbc.ini','w') as configfile:
#                         config.write(configfile)
#                 config[str(gid)][str(pbc)]='1'
#                 with open('pbc.ini','w') as configfile:
#                     config.write(configfile)
#                 msg = '已添加屏蔽词'
#                 sendmsg(msg,gid)
#     else:
#         msgs = '你没有管理员权限'
#         sendmsg(msg,gid)

# def dlpbc(pbc,uid,gid):
#     config.read('pbc.ini')
#     doadmin = 'admin'+str(gid)+str(uid)
#     if str(uid) == '2774737215' or config.has_option(str(gid),doadmin) == True :
#         if gid != None:
#             config.read('pbc.ini')
#             if config.has_option(str(gid),str(pbc)) == True:
#                 config.remove_option(str(uid),str(pbc))
#                 with open('pbc.ini','w') as configfile:
#                     config.write(configfile)
#             msg = '已移除屏蔽词'
#             sendmsg(msg,gid)
#         else:
#             msg = '你没有管理员权限'
#             sendmsg(msg,gid)


# def addadmin(doadmin,uid,gid):
#     config.read('pbc.ini')
#     user = 'admin'+str(gid)+str(uid)
#     if gid != None:
#         if str(uid) == '2774737215' or config.has_option(str(gid),user) == True :
#             config.read('pbc.ini')
#             if config.has_section(gid)==False:
#                 config[gid]={'1':'1'}
#                 with open('pbc.ini','w') as configfile:
#                     config.write(configfile)
#             if config.has_option(str(gid),doadmin) ==False:
#                 config[str(gid)][str(uid)]=1
#                 with open('pbc.ini','w') as configfile:
#                     config.write(configfile)
#                 msg = '该群管理员已创建'
#                 sendmsg(msg,gid)
#             else:
#                 msg = '该群管理员已经创建'
#                 sendmsg(msg,gid)
#         else:
#             msg = '你没有管理员权限'
#             sendmsg(msg,gid)