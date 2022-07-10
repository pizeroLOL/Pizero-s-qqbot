import time

from pkg_resources import fixup_namespace_packages
import GoCqhttpApi

'''
uid是发给谁的uid
gid是用来规定发哪个群里，如果把gid删除，则为使用私信发送，没有好友就直接报错
'''

uid = '1060432245'
gid = '1004741240'

'''
下面 GoCqhttpApi.sendmsg 中，第一格为发送的信息，第二格为uid，第三格为gid
time.sleep(1) 是在你怕被封号的时候加上，如果你不怕被封，随便用，不加也行
'''

'''以下是单次发送的例子'''
GoCqhttpApi.sendmsg('你有没有对可乐兔三番五次的禁言感到烦躁，%0A你有没有对可乐兔在滥用权力感到愤怒，%0A你有没有听到被禁言者在悲鸣。%0A所以，让我们一起说',uid,gid)

'''以下是多次发送同一个句子的例子，变量为massage，当然可以像上面那个一样。这里为了美观用了变量。
time.sleep(1) 是在你怕被封号的时候加上，如果你不怕被封，随便用，不加也行'''
for msg in range(100):
    message = '可乐兔，我日你先人'
    GoCqhttpApi.sendmsg(message,uid,gid)
    # time.sleep(1)

'''以下是一次按照顺序发送指定列表里的字符,msgs是表'''

msgs = ['你有没有对可乐兔三番五次的禁言感到烦躁',
'你有没有对可乐兔在滥用权力感到愤怒',
'你有没有听到被禁言者在悲鸣']
# 以下是循环
for msg in msgs:
    message = msg
    GoCqhttpApi.sendmsg(message,uid,gid)
    # time.sleep(1)

'''以下下是死循环，用于折磨人'''
while True:
    for msg in msgs:
        message = msg
        GoCqhttpApi.sendmsg(message,uid,gid)
        # time.sleep(1)


'''
tips:不需要的记得注释哦，虽然你可能没啥问题，但是可能看得不舒服，让我们一起说，so fuck you xxx.
'''