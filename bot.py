import check
import server
import configparser

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