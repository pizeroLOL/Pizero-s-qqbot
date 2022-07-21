import requests,configparser,time

config = configparser.ConfigParser()
config.read('app-config.cfg')

uid_topsecret = config['request']
host = str(uid_topsecret['request-host'])
post = str(uid_topsecret['request-post'])

global_uid = None
msg_step = 0

def sendmsg(msg,uid,gid = None):
    '''发送消息，当gid为空时发送私聊消息'''
    '''刹车'''
    if time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) != diff_time and gid == global_uid:
        diff_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        msg_step = msg_step + 1
    else:
        msg_step = 0
        global_uid = uid
    if msg_step == 2:
        time.sleep(1)
        return sendmsg('触发频率过高请再发一次')
    '''正常发送流程'''
    if gid != None:
        requests.get('http://{0}:{1}/send_group_msg?group_id={2}&message={3}'.format(host,post,gid,msg))
    else :
        requests.get('http://{0}:{1}/send_private_msg?user_id={0}&message={1}'.format(host,post,uid,msg))

def poke(uid,gid = None):  #戳一戳
    '''戳一戳，uid为被戳的人，当gid为空时发送私聊戳一戳'''
    msg='[CQ:poke,qq='+uid+']'
    sendmsg(msg,uid,gid)
# [CQ:poke,qq=<qq号>] 戳一戳的cq代码

def songs(message,uid,gid = None):
    '''点歌，检测前二到五位是否是指定字符串，空一格后面数字是song id'''
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
