import time
import GoCqhttpApi
import jrrp
import configparser

config = configparser.ConfigParser()
config.read('app-config.cfg')

default_qq='123456789'

def initialization(section,option): # 初始化
    if section == 'uid':
        if option == 'Mascot_id':
            config['uid']['Mascot_id'] = default_qq
        elif option == 'admin_id':
            config['uid']['admin_id'] = default_qq
        elif option == 'robot_id':
            config['uid']['robot_id'] = default_qq
        else:
            config['uid'] = {'Mascot_id':default_qq,
                             'admin_id':default_qq,
                             'robot_id':default_qq}
    # elif section == 'Mascot':
    #     if option == 'fuck_Mascot_id':
    #         config['Mascot']
    with open('app-config.cfg','w') as configfile:
        config.write(configfile)

# 检查config完整性
## 检查uid表完整性
if config.has_section('uid') == True :
    initialization_name='uid'
    if config.has_option(initialization_name,'Mascot_id') == False:
        initialization(initialization_name,'Mascot_id')
    if config.has_option(initialization_name,'admin_id') == False:
        initialization(initialization_name,'admin_id')
    if config.has_option(initialization_name,'robot_id') == False:
        initialization(initialization_name,'robot_id')
else:
    initialization('uid')

# if config.has_section('Mascot')

# 参数导入
uid_topsecret = config['uid']
Mascot_id = str(uid_topsecret['Mascot_id'])
admin_id = str(uid_topsecret['admin_id'])
robot_id = str(uid_topsecret['robot_id'])
at_robot = '[CQ:at,qq='+robot_id+']'

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
        uid = Mascot_id
        return GoCqhttpApi.poke(uid,gid)
    elif message[0:5] == '可乐兔三连' or message[0:5] == '可樂兔三連':
        # if fuck_klt == True:
        msgs=['可乐兔整合包更了吗','可乐兔模组更了吗','提学分了吗']
        for msg in msgs:
            GoCqhttpApi.sendmsg(msg,uid,gid)
            time.sleep(1)
    
    elif message[0: 5] == '#poke' or message[0:2] == '#戳' or message[0:4] == '#戳一戳' :
        return others_poke(message,uid,gid)

def helps(uid,gid): #帮助
    msg='https://docs.qq.com/doc/DVkJTdGxobFlHVm10?groupUin=4H%25252FXMn9Z1JVTKy99sMDYfg%25253D%25253D&ADUIN=2774737215&ADSESSION=1655715075&ADTAG=CLIENT.QQ.7824_.0&ADPUBNO=27190&u=9786d41c28d7486b8ab871637dd2ed35'
    GoCqhttpApi.sendmsg(msg,uid,gid)

def good_night(uid,gid):  
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