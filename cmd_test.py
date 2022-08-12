import check
import server
import os


def command_test():
    check.check()
    while True:
        msg = input('> ')
        if msg == 'exit':
            os._exit(0)
        server.keyword(msg, '131321', '413212313132')
