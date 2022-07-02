import pandas as pd
import time,os

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
    print(msglog)
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
    print(msglog)
    msglog = msglog.reindex_like(msglog)
    msglog.to_csv(file_path,index=None)