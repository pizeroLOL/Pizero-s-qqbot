import configparser

config = configparser.ConfigParser()
config.read('app-config.cfg')

default_qq='123456789'
default_type = 'True'

def initialization(section,option): # 初始化
    if section == 'uid':
        if option == 'Mascot_id':
            config['uid']['Mascot_id'] = default_qq
        elif option == 'admin_id':
            config['uid']['admin_id'] = default_qq
        elif option == 'robot_id':
            config['uid']['robot_id'] = default_qq
        elif option == 'all':
            config['uid'] = {'Mascot_id':default_qq,
                             'admin_id':default_qq,
                             'robot_id':default_qq}
    elif section == 'klt':
        if option == 'uid':
            config['klt']['uid'] = default_qq
        elif option == 'fuck_type':
            config['klt']['fuck_type'] = default_type
        elif option == 'all':
            config['klt'] = {'uid':default_qq,
                             'fuck_type':default_type}
    elif section == 'Mascot':
        if option == 'poke':
            config['Mascot']['poke_type'] = default_type
        elif option == 'all':
            config['Mascot']={'poke_type':default_type}
    elif section == 'main':
        if option == 'host':
            config['main']['host'] = '127.0.0.1'
        elif option == 'port':
            config["main"]["port"] = '20301'
        elif option == 'debug':
            config["main"]["debug"] = default_type

    with open('app-config.cfg','w') as configfile:
        config.write(configfile)

# 检查config完整性
## 检查uid表完整性
def check():
    if config.has_section('main') == True:
        initialization_name = 'main'
        if config.has_option(initialization_name,'host') == False:
            initialization(initialization_name,'host')
        if config.has_option(initialization_name, "port") == False:
            initialization(initialization_name, "port")
        if config.has_option(initialization_name, "debug") == False:
            initialization(initialization_name, "debug")
    else:
        initialization('main','all')
    if config.has_section('uid') == True :
        initialization_name='uid'
        if config.has_option(initialization_name,'Mascot_id') == False:
            initialization(initialization_name,'Mascot_id')
        if config.has_option(initialization_name,'admin_id') == False:
            initialization(initialization_name,'admin_id')
        if config.has_option(initialization_name,'robot_id') == False:
            initialization(initialization_name,'robot_id')
    else:
        initialization('uid','all')

    ## 检查吉klt选项
    if config.has_section('klt') == True:
        initialization_name = "klt"
        if config.has_option(initialization_name, "uid") == False:
            initialization(initialization_name,'uid')
        if config.has_option(initialization_name, 'fuck_type') == False:
            initialization(initialization_name,'fuck_type')
    else:
        initialization('klt','all')

    ##检查吉祥物选项
    if config.has_section('Mascot') == True:
        initialization_name = 'Mascot'
        if config.has_option(initialization_name,'poke_type') == False:
            initialization(initialization_name,'poke_type')
    else:
        initialization(initialization_name,'all')