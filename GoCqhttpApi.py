import requests

def sendmsg(msg,uid,gid = None):
    if gid != None:
        requests.get('http://127.0.0.1:20300/send_group_msg?group_id={0}&message={1}'.format(gid,msg))
    else :
        requests.get('http://127.0.0.1:20300/send_private_msg?user_id={0}&message={1}'.format(uid,msg))

def poke(uid,gid = None):  #戳一戳
    msg='[CQ:poke,qq='+uid+']'
    sendmsg(msg,uid,gid)
# [CQ:poke,qq=<qq号>] 戳一戳的cq代码

def songs(message,uid,gid = None):
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










