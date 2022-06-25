from email import message
import time
import requests
import random
import configparser

config = configparser.ConfigParser()

## rp-人品
## timeis-时间
admin='2774737215'
bot_qq="3282686818"

def keyword(message,uid,gid = None):
    uid=str(uid)
    if gid != None:
        gid=str(gid)
    if message[0:5] == '#help' or message[0:3] == '#帮助' or message[0:3] == '#幫助' or message[0:5] == '' or message[0:5] == '#使用說明':
        return helps(uid,gid)

    elif message[0:21] == '[CQ:at,qq=3282686818]':
        return poke(uid,gid)

    elif message[0:4] == '今日人品' or message[0:4]=='jrrp':
        types='self'
        return jrrp(types,uid,gid)

    elif message[0:3] == '#点歌' or message[0:3] == '#點歌':
        message = message[4:]
        return songs(message,uid,gid)

    elif message[0:2] == '晚安':
        return good_night(uid,gid)

    elif message[0:5] == '#人品查询' or message[0:5] == '#rpcx' or message[0:5] == '#人品査詢':
        if len(message) > 8 :
            uid = message[6:]
            types='others'
        else:
            types='self'
        return jrrp(types,uid,gid)

    elif message[0:5] == '摸摸sms':
        uid = '3612079899'
        return poke(uid,gid)
    elif message[0:5] == '可乐兔三连' or message[0:5] == '可樂兔三連':
        msgs=['可乐兔整合包更了吗','可乐兔模组更了吗','提学分了吗']
        for msg in msgs:
            sendmsg(msg,uid,gid)
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


def sendmsg(msg,uid,gid):
    if gid != None:
        requests.get('http://127.0.0.1:20300/send_group_msg?group_id={0}&message={1}'.format(gid,msg))
    else :
        requests.get('http://127.0.0.1:20300/send_private_msg?user_id={0}&message={1}'.format(uid,msg))

def poke(uid,gid):  #戳一戳
    msg='[CQ:poke,qq='+uid+']'
    sendmsg(msg,uid,gid)
# [CQ:poke,qq=<qq号>] 戳一戳的cq代码

## 应用模块例子
#def xxxxx(xxx,xxx,xxx):  
    #msg=''
    #sendmsg(msg,uid,gid)

## msg为发送的信息
## uid为发送者
## gid为收到消息的群

def helps(uid,gid): #帮助
    msg='https://docs.qq.com/doc/DVkJTdGxobFlHVm10?groupUin=4H%25252FXMn9Z1JVTKy99sMDYfg%25253D%25253D&ADUIN=2774737215&ADSESSION=1655715075&ADTAG=CLIENT.QQ.7824_.0&ADPUBNO=27190&u=9786d41c28d7486b8ab871637dd2ed35'
    sendmsg(msg,uid,gid)


def songs(message,uid,gid):
    if message[:2] == 'QQ' or message[:2] == 'qq':
        song_id = message[3:]
        song_type = 'qq'
    elif message[:4] == 'QQ音乐' or message[:4] == 'qq音乐' or message[:4] == 'qqyy' or message[:4] == 'QQ音樂'or message[:4] == 'qq音樂':
        song_id = message[5:]
        song_type = 'qq'
    elif message[:5] == '网易云音乐' or message[:5] == 'wyyyy' or message[:5] == '網易雲音樂':
        song_id = message[6:]
        song_type = '163'
    elif message[:2] == '网易' or message[:2] == 'wy' or message[:2] == '網易':
        song_id = message[3:]
        song_type = '163'
    msg = '[CQ:music,type='+song_type+',id='+song_id+']'
    sendmsg(msg,uid,gid)

## [CQ:music,type=源,id=音乐id]


def jrrp(types,uid,gid):  #今日人品
    timeis=time.strftime("%Y-%m-%d", time.localtime()) #收到时间，格式为年-月-日
    config.read('jrrp.ini') #读取jrrp.ini
    if config.has_section(timeis) == False: #判断文件中是否有时间相对应的表，没有则创捷
        config[timeis]={'1':'1'} #创建一个表并创建一个项：1:1
        with open('jrrp.ini','w') as configfile: #写入jrrp.ini
            config.write(configfile)
    if config.has_option(timeis, str(uid)) == False : #有没有uid对应的项,没有就创建
        rp = random.randrange(0,100,1) #获得一个随机数
        config[timeis][str(uid)]=str(rp) #创建一个uid所对的项
        with open('jrrp.ini','w') as configfile:
            config.write(configfile)
    if types == 'self':
        topsecret = config[ timeis ] #选中当前时间的表
        rp=topsecret[str(uid)] #发出将人品与表中uid相对
        rp=str(rp)
        if gid != None:
            msg='[CQ:at,qq='+uid+']你的人品为'+rp
            sendmsg(msg,uid,gid)
            if int(rp) < 20:
                poke(uid,gid)
        else:
            msg='你的人品为'+rp
            sendmsg(msg,uid)
    elif types == 'others':
        topsecret = config[ timeis ] #选中当前时间的表
        rp=topsecret[str(uid)] #发出将人品与表中uid相对
        rp=str(rp)
        msg=str(uid)+'的人品为'+rp
        sendmsg(msg,uid,gid)

def good_night(uid,gid):  
    msg='晚安'
    sendmsg(msg,uid,gid)

def others_poke(message,uid,gid):
    if message[0: 5] == '#poke' :
        uid = message[5:]
    elif message[0:2] == '#戳' :
        uid = message[3:]
    elif message[0:4] == '#戳一戳' :
        uid = message[4:]
    poke(uid,gid)

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

