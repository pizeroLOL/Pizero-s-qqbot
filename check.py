import configparser
import pandas as pd
import os


def check():
    '''检查配置文件'''
    # 导入配置文件
    config = configparser.ConfigParser()
    config.read('app-config.cfg', encoding='utf-8')

    '''初始化
    默认变量在第十行，变量名为configlist，包含Function、id、main、request'''
    # 默认初始化变量
    default_qq = '123456789'
    default_type = 'True'
    default_host = '127.0.0.1'
    configlist = ['Function', 'id', 'main', 'request']
    for i in configlist:
        '''i为上方的configlist'''
        if i == 'Function':
            lib = ['jrrp', 'look_for_group_type', 'fuck_type', 'poke_type',
                   'debug', 'msglog_private_type', 'msglog_group_type']
        elif i == 'id':
            lib = ['Mascot_id', 'admin_id', 'robot_id',
                   'klt_id', 'look_for_group_id']
        elif i == 'main':
            lib = ['host', 'port']
        elif i == 'request':
            lib = ['request-host', 'request-post']

        if config.has_section(i) == False:  # 检测是否有当前表
            config.add_section(i)
        for n in lib:
            '''n为上方lib变量'''
            if config.has_option(i, n) == False and i == 'Function':
                config[i][n] = default_type
            elif config.has_option(i, n) == False and i == 'id':
                config[i][n] = default_qq
            elif config.has_option(i, n) == False and 'host' in n:
                config[i][n] = default_host
            elif config.has_option(i, n) == False and "port" in n and i == 'main':
                config[i][n] = '20301'
            elif config.has_option(i, n) == False and n == 'request-post':
                config[i][n] = '20300'
    '''保存为app-config.cfg'''
    with open('app-config.cfg', 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    '''QAs'''
    file_path = './QAs.csv'
    if os.path.isfile(file_path) == False:
        tmpfm = pd.DataFrame({
            'Q': ['晚安'],
            'A': ['晚安~']
        })
        tmpfm.to_csv(file_path, index=None, mode='w', encoding='utf8')


check()
