import sys
import web.webserver as server
import os
import config.reader as configreader

# FILEPATH = path to the src directory
FILEPATH = os.path.abspath(os.path.dirname(__file__)) + '/'
# WEB_CONFIG_PATH = path to the web directory inside src directory
WEB_CONFIG_PATH = FILEPATH + "web/"
# DB_CONFIG_PATH = path to the db directory inside src directory
DB_CONFIG_PATH = FILEPATH + "db/"

# Receives commandline arguments and executes commands based on them
# 'config' = asks user to fill required configuration
# 'start' = starts to listen for connections
def main(args):
    if len(args) == 1:
        if args[0] == 'config':
            configreader.write_config(WEB_CONFIG_PATH, DB_CONFIG_PATH)
        elif args[0] == 'start':
            if configreader.config_exists(WEB_CONFIG_PATH, DB_CONFIG_PATH):
                server.listen()
            else:
                print("Configuration files missing.")

if __name__ == '__main__':
    main(sys.argv[1:])