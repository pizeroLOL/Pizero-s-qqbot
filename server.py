from flask import Flask, request
import QQbotApp,configparser,GoCqhttpApi,jrrp,time,os
import pandas as pd

# 导入配置文件
config = configparser.ConfigParser()
config.read('app-config.cfg')

# 默认初始化变量
default_qq='123456789'
default_type = 'True'
default_host = '127.0.0.1'

configlist = ['Function','id','main','request']

def check():
    #初始化
    for i in configlist:
        if i == 'Function':
            lib = ['jrrp','look_for_group_type','fuck_type','poke_type','debug']
        elif i == 'id':
            lib = ['Mascot_id','admin_id','robot_id','klt_id','look_for_group_id']
        elif i == 'main':
            lib = ['host','port']
        elif i == 'request':
            lib = ['request-host','request-post']

        if config.has_section(i) == False:
            config.add_section(i)
        for n in lib:
            if config.has_option(i, n) == False and i == 'Function':
                config[i][n] = default_type
            elif config.has_option(i,n) == False and i == 'id':
                config[i][n] = default_qq
            elif config.has_option(i, n) == False and 'host' in n:
                config[i][n] = default_host
            elif config.has_option(i, n) == False and "port"in n and i == 'main':
                config[i][n] = '20301'
            elif config.has_option(i, n) == False and n == 'request-post':
                config[i][n] = '20300'

    with open('app-config.cfg','w') as configfile:
        config.write(configfile)

# 删除初始化变量并作检查
check()
del default_qq,default_type,default_host,configlist

# 参数导入
## uid表
uid_topsecret = config['id']
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

# 其他全局变量
diff_time = None
msg_step = 0

# main表
main_topsecret = config['main']

def keyword(message,uid,gid = None):
    global diff_time,msg_step
    uid=str(uid)
    if gid != None:
        gid=str(gid)

    if time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) != diff_time and gid == look_for_group_id:
        diff_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        msg_step = msg_step + 1
    else:
        msg_step = 0
    if msg_step == 2:
        return tell_admin(admin_id,uid,gid)

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

def tell_admin(admin_id,uid,gid):
    msg =  '[CQ:at,qq='+admin_id+'] 每秒发送超过3条信息，关注一下'
    GoCqhttpApi.sendmsg(msg,uid,gid)


# 记录信息发送
def group(msg,uid,gid):
    timeis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # columns = ['msg','uid','gid']
    file_path = './msglog/msglog-group'+time.strftime("%Y-%m-%d", time.localtime())+'.csv'
    tmpfm = pd.DataFrame({
        'message':[msg],
        'time':[timeis],
        'uid':[uid],
        'gid':[gid]
    })
    if os.path.exists('./msglog') == False:
        os.mkdir('msglog')
    if os.path.isfile(file_path) == True:
        msglog = pd.read_csv(file_path)
        msglog = pd.concat([msglog,tmpfm],ignore_index=True)
    else:
         msglog = tmpfm
    msglog = msglog.reindex_like(msglog)
    msglog.to_csv(file_path,index=None)

def private(msg,uid):
    timeis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # columns = ['msg','uid','gid']
    file_path = './msglog/msglog-private'+time.strftime("%Y-%m-%d", time.localtime())+'.csv'
    tmpfm = pd.DataFrame({
        'message':[msg],
        'time':[timeis],
        'uid':[uid]
    })
    if os.path.exists('./msglog') == False:
        os.mkdir('msglog')
    if os.path.isfile(file_path) == True:
        msglog = pd.read_csv(file_path)
        msglog = pd.concat([msglog,tmpfm],ignore_index=True)
    else:
         msglog = tmpfm
    msglog = msglog.reindex_like(msglog)
    msglog.to_csv(file_path,index=None)


# 服务端本体
app = Flask(__name__)

@app.route("/",methods=["POST"])
def return_app():
    ## 下面的request.get_json().get......是用来获取关键字的值用的，关键字参考上面代码段的数据格式
    if request.get_json().get('message_type') == 'private':# 如果是私聊信息		
        uid = request.get_json().get('sender').get('user_id') # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message') # 获取原始信息
        keyword(message, uid) # 将 Q号和原始信息传到我们的后台
        private(message,uid)
    if request.get_json().get('message_type') == 'group':# 如果是群聊信息
        gid = request.get_json().get('group_id') # 获取群号
        uid = request.get_json().get('sender').get('user_id') # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message') # 获取原始信息
        keyword(message, uid, gid) # 将 Q号和原始信息传到我们的后台
        group(message,uid,gid)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=Function_topsecret.getboolean('debug'), host=main_topsecret['host'], port=main_topsecret["port"])