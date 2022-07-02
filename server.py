from flask import Flask, request
import initialization,QQbotApp,Record,configparser

config = configparser.ConfigParser()
config.read('app-config.cfg')

initialization.check()
main_topsecret = config['main']

app = Flask(__name__)

@app.route("/",methods=["POST"])
def return_app():
    time = request.get_json().get('time')
    ## 下面的request.get_json().get......是用来获取关键字的值用的，关键字参考上面代码段的数据格式
    if request.get_json().get('message_type') == 'private':# 如果是私聊信息		
        uid = request.get_json().get('sender').get('user_id') # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message') # 获取原始信息
        QQbotApp.keyword(message, uid) # 将 Q号和原始信息传到我们的后台
        Record.private(message,uid)
    if request.get_json().get('message_type') == 'group':# 如果是群聊信息
        gid = request.get_json().get('group_id') # 获取群号
        uid = request.get_json().get('sender').get('user_id') # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message') # 获取原始信息
        QQbotApp.keyword(message, uid, gid) # 将 Q号和原始信息传到我们的后台
        Record.group(message,uid,gid)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=main_topsecret.getboolean('debug'), host=main_topsecret['host'], port=main_topsecret["port"])