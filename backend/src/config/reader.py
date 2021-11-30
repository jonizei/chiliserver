
# Reads config file and returns it in a
# dictionary format
def get_config(filepath):
    with open(filepath, 'r') as config_file:
        return create_config_dict(config_file.read())

# Creates a dictionary using the contents of 
# the confing file
def create_config_dict(data):
    config = {}
    lines = data.split("\n")

    for line in lines:
        line = line.replace(" ", "")
        tokens = line.split("=")
        config.update({tokens[0] : tokens[1]})

    return config