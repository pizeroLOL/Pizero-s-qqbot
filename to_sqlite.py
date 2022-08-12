from sqlalchemy import create_engine
import pandas as pd
import os

import configparser
config = configparser.ConfigParser()


engine = create_engine('sqlite:///bot.db')


def ini2sqlite():
    configlist = ['Function', 'id', 'main', 'request']
    if os.path.isfile('./jrrp.ini') == False:
        raise PermissionError('you don\'t have jrrp.ini')
    config.read('jrrp.ini', encoding='utf-8')
    for sections in config.sections():
        if sections in configlist:
            continue
        for key in config[sections]:
            if key == '1':
                continue
            df = pd.DataFrame([{
                'date': sections,
                'id': key,
                'rp': config[sections][key],
            }])
            df.to_sql('jrrp', engine, if_exists='append', index=False)


def csv2sqlite():
    if os.path.exists('./msglog') == False:
        raise Exception('you don\'t have ./msglog')
    for folder in os.listdir('./msglog'):
        path = './msglog/'+folder
        for a, b, files in os.walk(path):
            if files == []:
                continue
            for file in files:
                file_path = path + '/' + file
                print(file_path)
                if file[-4:] != '.csv':
                    print('file '+file+' is not a CSV file')
                    continue
                df = pd.read_csv(file_path)
                df.to_sql(folder, engine, if_exists='replace', index=False)


def convert_flow():
    ini2sqlite()
    csv2sqlite()


if __name__ == '__main__':
    ini2sqlite()
    csv2sqlite()
