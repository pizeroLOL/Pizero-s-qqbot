import time
import requests
import GoCqhttpApi

uid = ''
gid = ''
msgs = [' ',' ',' ',' ']

for msg in msgs:
    message = msg
    GoCqhttpApi.sendmsg(message,uid,gid)
    time.sleep(1)