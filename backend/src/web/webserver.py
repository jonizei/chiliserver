from http.server import BaseHTTPRequestHandler, HTTPServer
import db.connector as dbconnector
import json
import os
import config.reader as configreader
import outlet.manager as outletmanager

# FILEPATH = path to the web directory inside src directory
# CONFIG_FILE = path to the web server config file
# CONFIG = dictionary which contains web server configuration
# OUTLETMGR = object which contains methods to control outlet info
# WEBUI_DIR = path to the directory of project ui files
FILEPATH = os.path.abspath(os.path.dirname(__file__)) + '/'
CONFIG_FILE = FILEPATH + "webconfig.txt"
CONFIG = configreader.get_config(CONFIG_FILE)
OUTLETMGR = outletmanager.OutletManager()
WEBUI_DIR = FILEPATH + "webui/"

# WebServer class which handles all GET and POST requests
class WebServer(BaseHTTPRequestHandler):

    # Method which handles all GET requests
    def do_GET(self):
        
        if self.path == "/":
            self.send_file("index.html")

        # Sends records as a json to a client
        elif self.path == "/get-records":
            records = self.get_records(as_json=True)
            if records is not False:
                self.set_headers(200, [("Content-Type", "application/json"), ("Access-Control-Allow-Origin", "*")])
                self.wfile.write(records.encode("utf-8"))
            else:
                self.server_response(500, "")

        # Sends outlets as a json to a client
        elif self.path == "/get-outlets":
            self.send_outlets()

        elif self.is_resource_file(self.path):
            self.send_file(self.path[1:])

        else:
            self.send_file_not_found()

    # Method which handles all POST requests
    def do_POST(self):

        content_len = int(self.headers.get("Content-Length"))
        post_body = None

        if content_len > 0:
            post_body = self.rfile.read(content_len)

        # Receives records as a json from a client
        # Saves record information to a database
        # Sends outlets as a json to a client
        if self.path == "/post-record":
            if post_body is not None:
                record = json.loads(post_body)
                print(f"Record received: {record} \n")
                self.save_record(record)
                outlets_json = json.dumps(OUTLETMGR.check_triggers(record))
                self.server_response(200, outlets_json)
            else:
                self.server_response(400, "")
            

        # Receives outlets as a json from a client
        # Saves the json to a file
        elif self.path == "/update-outlets":
            if post_body is not None:
                outlets = json.loads(post_body)
                for out in outlets:
                    OUTLETMGR.update_outlet(out)
                OUTLETMGR.save_outlets()
                self.server_response(200, "")
            
    # Takes response code and headers as parameters
    # and sends them to a client.
    # Headers are array of Tuples
    def set_headers(self, response_code, headers):
        self.send_response(response_code)
        for h in headers:
            self.send_header(h[0], h[1])
        self.end_headers()

    # Retrieves records from a database and sends them
    # to a client
    # 'as_json' parameter determines if records are in
    # json or in a dictionary format
    def get_records(self, as_json=False):
        db = dbconnector.DBConnection()
        result = db.fetch_records(as_json)
        db.close()
        return result

    # Takes a filename as a parameter, reads the file
    # from web ui directory and sends it to a client
    def send_file(self, filename):
        content_type = self.get_content_type(filename)
        if not content_type is False:
            with open(WEBUI_DIR + filename, "rb") as f:
                self.set_headers(200, [content_type, ("Access-Control-Allow-Origin", "*")])
                self.wfile.write(f.read())
        else:
            self.send_file_not_found()

    # Returns content-type based on the file extension
    def get_content_type(self, filename):
        tokens = filename.split(".")
        if len(tokens) > 1:
            extension = tokens[-1]

            if extension == 'html':
                return ("Content-Type", "text/html")
            elif extension == 'js':
                return ("Content-Type", "application/javascript")
            elif extension == 'css':
                return ("Content-Type", "text/css")
            
        return False


    # Takes a record (dictionary) as a parameter and saves it
    # to a database
    def save_record(self, record : dict()):
        db = dbconnector.DBConnection()
        db.insert_record(record)
        db.close()

    # Load a outlets json file and sends it to client
    def send_outlets(self):
        self.set_headers(200, [("Content-Type", "application/json"), ("Access-Control-Allow-Origin", "*")])
        outlet_json = json.dumps(OUTLETMGR.load_outlets())
        self.wfile.write(bytes(outlet_json, "utf-8"))

    def server_response(self, code, payload):
        self.set_headers(code, [("Content-Type", "application/json"), ("Access-Control-Allow-Origin", "*")])
        self.wfile.write(payload.encode("utf-8"))

    def is_resource_file(self, path):
        filename = path[1:]
        resources = os.listdir(WEBUI_DIR)
        if len(resources) > 0:
            return filename in resources
        
        return False
    
    def send_file_not_found(self):
        self.set_headers(404, [("Content-Type", "text/html")])
        self.wfile.write("<h1>Page not found.</h1>".encode("utf-8")) 


# Starts listening on given hostname and port
# Can be interrupted with keyboard (Ctrl + C)
def listen():
    webserver = HTTPServer((CONFIG["HOSTNAME"], int(CONFIG["PORT"])), WebServer)
    webserver.timeout = 60
    print(f"Listening on port: {CONFIG['PORT']}")
    
    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass

    webserver.server_close()

