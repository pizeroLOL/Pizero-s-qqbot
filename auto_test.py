import random
import check
import server
import GoCqhttpApi
import os

GoCqhttpApi.test()

msgs = ['[CQ:at,qq=123456789]', 'jrrp', '今日人品', '#点歌 wyyyy 132456789',
        '#点歌 wyy 132456789', '#点歌 wy 132456789', '#点歌 qq 132456789',
        '#点歌 qqyy 132456789', '#人品查询', '#人品查询 12346579', '摸摸吉祥物',
        '可乐兔三连', '#poke', '#poke 13254448', '#top20', '#月发信息表', '#活跃时间',
        '#活跃时间散点图', '#全部问题', '#消息查询', '#消息查询 jrrp']

def test(to_str = None):
    for i in range(len(msgs)):
        uid = random.randint(10000, 1000000000)
        gid = random.randint(10000, 1000000000)
        if to_str != None:
            uid = str(uid)
            gid = str(gid)
        server.group(msgs[i],uid,gid)
        server.keyword(msgs[i], uid, gid)
        server.private(msgs[i],uid)
        server.keyword(msgs[i], uid)

def one_test():
    test()
    print('\n\n\nfinished int\n\n\n')
    test('str')    
    print('\n\n\nfinished str\n\n\n')

one_test()
check.check()
print('\n\n\ncheck!\n\n\n')
one_test()