import check
import server
import os

uid = '131321'
gid = '413212313132'
def command_test():
    check.check()
    while True:
        msg = input('> ')
        if msg == 'exit':
            os._exit(0)
        server.group(msg,uid,gid)
        server.keyword(msg,uid,gid)
