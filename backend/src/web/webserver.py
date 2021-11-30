from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
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
        
        # Sends records as a json to a client
        if self.path == "/get-records":
            self.set_headers(200, [("Content-Type", "application/json"), ("Access-Control-Allow-Origin", "*")])
            records = self.get_records(as_json=True)
            self.wfile.write(records.encode("utf-8"))

        # Sends outlets as a json to a client
        elif self.path == "/get-outlets":
            self.send_outlets()

        else:
            self.set_headers(404, [("Content-Type", "text/html")])
            self.wfile.write("<h1>Page not found.</h1>")

    # Method which handles all POST requests
    def do_POST(self):

        content_len = int(self.headers.get("Content-Length"))
        post_body = self.rfile.read(content_len)

        # Receives records as a json from a client
        # Saves record information to a database
        # Sends outlets as a json to a client
        if self.path == "/post-record":
            record = json.loads(post_body)
            print(f"Record received: {record} \n")
            self.save_record(record)
            outlets_json = json.dumps(OUTLETMGR.check_triggers(record))
            self.set_headers(200, [("Content-Type", "application/json")])
            self.wfile.write(outlets_json.encode("utf-8"))

        # Receives outlets as a json from a client
        # Saves the json to a file
        elif self.path == "/update-outlets":
            outlets = json.loads(post_body)
            for out in outlets:
                OUTLETMGR.update_outlet(out)
            OUTLETMGR.save_outlets()
            self.set_headers(200, [("Content-Type", "text/html"), ("Access-Control-Allow-Origin", "*")])
            self.wfile.write("".encode("utf-8"))
            
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
        f = open(WEBUI_DIR + filename, "r")
        self.wfile.write(bytes(f.read(), "utf-8"))

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

