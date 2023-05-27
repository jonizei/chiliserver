import datetime
import json
from json import JSONEncoder
import os
import config.reader as configreader
import psycopg2

# FILEPATH = path to the db directory inside of src directory
# CONFIG_FILE = path to the database connection config file
FILEPATH = os.path.abspath(os.path.dirname(__file__)) + '/'
CONFIG_FILE = FILEPATH + "dbconfig.txt"

# This class connects to a given database
# Contains methods that handles communication with a database
class DBConnection():

    ERROR_CODES = {
        100: "Unable to connect to database",
        101: "No database connection found"
    }

    # Reads database info from config file
    # Tries to establish connection with a given database
    def __init__(self):
        self.config = configreader.get_config(CONFIG_FILE)
        self.db = None
        
        try:
            self.db = psycopg2.connect(host=self.config["DB_HOST"], user=self.config["DB_USER"], password=self.config["DB_PASS"], database=self.config["DB_NAME"])
        except Exception:
            self.error('CONNECTION', 100)


    # Tries to insert new record to a database
    def insert_record(self, record):
        if self.db is not None:
            cursor = self.db.cursor()
            query = (f"INSERT INTO {self.config['DB_TABLE']} (air_temperature, air_pressure, humidity, light) VALUES({self.record_to_string(record)})")
            cursor.execute(query)
            self.db.commit()
        else:
            self.error('INSERT RECORD', 101)

    # Fetches all databases from the postgres server
    def get_databases(self):
        if self.db is not None:
            cursor = self.db.cursor()
            query = (f"SELECT * FROM {self.config['DB_NAME']}")
            cursor.execute(query)
            self.db.commit()
        else:
            self.error('FETCH DATABASES', 101)

    # Creates string from dictionary values
    # For example: "value1, value2, value3"
    def record_to_string(self, record):
        return str(record['air_temperature']) + "," + str(record['air_pressure']) + "," + str(record['humidity']) + "," + str(record["light"])

    # Tries to fetch records from a database
    # 'as_json' determines wheter the return value is as
    # a dictionary or in a json format
    def fetch_records(self, as_json=False):
        if self.db is not None:
            cursor = self.db.cursor()
            query = (f"SELECT * FROM {self.config['DB_TABLE']} ORDER BY record_time DESC")
            cursor.execute(query)

            records = self.build_records(cursor)

            if not as_json:
                return records 
            else:
                return json.dumps(records, indent=4, cls=DateTimeEncoder)
        else:
            self.error('FETCH RECORDS', 101)
            return False

    # Creates a dictionary from the database result
    def build_records(self, cursor):
        records = []

        for col in cursor:
            record = {"id" : col[0], "air_temperature" : float(col[1]), "air_pressure" : float(col[2]), "humidity" : float(col[3]), "light" : int(col[4]), "datetime" : col[5]}
            records.append(record)

        return records

    # Closes the database connection
    def close(self):
        if self.db is not None:
            self.db.close()

    def error(self, target, code):
        print(f"Error: %s (%s)" % (DBConnection.ERROR_CODES[code], target))


# This class json encoder for datetime object
class DateTimeEncoder(JSONEncoder):

    # This method turns datetime to a json string
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            simpledate = f"%s.%s.%s" % (self.format(obj.date().day), self.format(obj.date().month), obj.date().year) 
            simpletime = f"%s:%s:%s" % (self.format(obj.time().hour), self.format(obj.time().minute), self.format(obj.time().second))
            return f"%s - %s" % (simpledate, simpletime)
        
    def format(self, num):
        if num < 10:
            return f"0%d" % (num)
        
        return num