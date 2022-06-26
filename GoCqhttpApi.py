import time
import requests
import random
import configparser



## rp-人品
## timeis-时间



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

