import GoCqhttpApi,jrrp,time,configparser

config = configparser.ConfigParser()
config.read('app-config.cfg')

# 参数导入
## uid表
uid_topsecret = config['uid']
Mascot_id = str(uid_topsecret['Mascot_id'])
admin_id = str(uid_topsecret['admin_id'])
robot_id = str(uid_topsecret['robot_id'])
klt_id = str(uid_topsecret['klt_id'])
look_for_group_id = str(uid_topsecret['look_for_group_id'])
at_robot = '[CQ:at,qq='+robot_id+']'

# Function表
Function_topsecret = config['Function']
fuck_type = Function_topsecret.getboolean('fuck_type')
poke_type = Function_topsecret.getboolean('poke_type')

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
