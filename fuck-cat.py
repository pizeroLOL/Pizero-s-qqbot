import time
import requests

uid = '2081813727'
gid = '706894591'
msgs = ['⚡猫⚡仔⚡你⚡欠⚡我⚡的⚡章⚡节⚡用⚡什⚡么⚡还⚡','爷是催更小助手，快来和我一起刀猫仔8','你一刀~我一刀~','让猫仔下条消息就是更↗新↘小↗说↘']

def sendmsg(msg,uid,gid):
    if gid != None:
        requests.get('http://127.0.0.1:20300/send_group_msg?group_id={0}&message={1}'.format(gid,msg))
    else :
        requests.get('http://127.0.0.1:20300/send_private_msg?user_id={0}&message={1}'.format(uid,msg))


for msg in msgs:
    message = msg
    sendmsg(message,uid,gid)
    time.sleep(1)