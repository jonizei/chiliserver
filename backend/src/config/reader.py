from os.path import exists

# Name of the web configuration file
WEB_CONFIG_FILE = "webconfig.txt"
# Name of the database configuration file
DB_CONFIG_FILE = "dbconfig.txt"

# Required data for web configuration
WEB_CONFIG_DATA = {
    'HOSTNAME' : 'Server host address',
    'PORT' : 'Server host port'
}

# Required data for database configuration
DB_CONFIG_DATA = {
    'DB_USER' : 'Database username',
    'DB_PASS' : 'Database password',
    'DB_HOST' : 'Database host address',
    'DB_NAME' : 'Database name',
    'DB_TABLE' : 'Database table name'
}

# Reads config file and returns it in a
# dictionary format
def get_config(filepath):
    if exists(filepath):
        with open(filepath, 'r') as config_file:
            return create_config_dict(config_file.read())
    
    return {}

# Creates a dictionary using the contents of 
# the confing file
def create_config_dict(data):
    config = {}
    lines = data.split("\n")
    lines = [x for x in lines if x]

    for line in lines:
        line = line.replace(" ", "")
        tokens = line.split("=")
        config.update({tokens[0] : tokens[1]})

    return config

# Writes configuration data to a file
def write_config_file(filepath, data):
    with open(filepath, 'w') as config_file:
        for key in data.keys():
            config_file.write(f"%s = %s\n" % (key, data[key]))

# Asks user to fill required configuration data and saves them to files
# Creates configuration file for a web server
# Creates configuration file for a database
def write_config(web_path, db_path):
    web_data = {}
    db_data = {}

    print("Web server configuration:")
    print("=========================")
    
    for key in WEB_CONFIG_DATA.keys():
        print(f"%s: " % (WEB_CONFIG_DATA[key]))
        tmp = input()
        web_data[key] = tmp.strip()

    for key in DB_CONFIG_DATA.keys():
        print(f"%s: " % (DB_CONFIG_DATA[key]))
        tmp = input()
        db_data[key] = tmp.strip()

    write_config_file(web_path + WEB_CONFIG_FILE, web_data)
    write_config_file(db_path + DB_CONFIG_FILE, db_data)

# Checks if both configuration files exists
def config_exists(web_path, db_path):
    if exists(web_path + WEB_CONFIG_FILE) and exists(db_path + DB_CONFIG_FILE):
        return True

    return False
