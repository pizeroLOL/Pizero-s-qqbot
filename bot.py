import check
import server
import configparser
import auto_test
import cmd_test
import sys


def start():
    config = configparser.ConfigParser()
    config.read('app-config.cfg')
    check.check()

    # Function表
    Function_topsecret = config['Function']
    server_debug_type = Function_topsecret.getboolean('debug')

    # main表
    main_topsecret = config['main']
    server_host = main_topsecret['host']
    server_post = main_topsecret["port"]

    server.app.run(debug=server_debug_type, host=server_host, port=server_post)


if len(sys.argv) != 2:
    start()
else:
    match sys.argv[1]:
        case '--help' | '-h':
            print('-a\t--auto-test\t执行自动测试脚本\n-c\t--command-test\t手动命令行测试')
        case '--auto-test' | '-a':
            auto_test.test_flow()
        case '--command-test' | '-c':
            cmd_test.command_test()
