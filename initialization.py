import configparser

config = configparser.ConfigParser()
config.read('app-config.cfg')

default_qq='123456789'
default_type = 'True'
default_host = '127.0.0.1'

configlist = ['uid','klt','Mascot','main','request','Function']
config.defaults()

def check():
    for i in configlist:
        if i == 'uid':
            lib = ['Mascot_id','admin_id','robot_id']
        elif i == 'klt':
            lib = ['uid','fuck_type']
        elif i == 'Mascot':
            lib = ['poke_type']
        elif i == 'main':
            lib = ['host','port','debug']
        elif i == 'request':
            lib = ['request-host','request-post']
        elif i == 'Function':
            lib = ['jrrp','look_for_group_id','look_for_group_type']
        dic = None
        if config.has_section(i) == False:
            config.add_section(i)
        for n in lib:
            if config.has_option(i,n) == False and 'id' in n:
                config[i][n] = default_qq
            elif config.has_option(i, n) == False and ('type' in n or n == 'debug' or n == 'jrrp'):
                config[i][n] = default_type
            elif config.has_option(i, n) == False and 'host' in n:
                config[i][n] = default_host
            elif config.has_option(i, n) == False and "port"in n and i == 'main':
                config[i][n] = '20301'
            elif config.has_option(i, n) == False and n == 'request-post':
                config[i][n] = '20300'

    with open('app-config.cfg','w') as configfile:
        config.write(configfile)
