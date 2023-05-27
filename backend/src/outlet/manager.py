import os
import json
from datetime import datetime, timedelta

# FILEPATH = path to the outlet dictionary inside src directory
# OUTLETS_FILE = path to the outlets json file
FILEPATH = os.path.abspath(os.path.dirname(__file__)) + '/'
OUTLETS_FILE = FILEPATH + "outlets.json"

# Dictionary for weekdays 
WEEKDAYS = {
    0: "MONDAY",
    1: "TUESDAY",
    2: "WEDNESDAY",
    3: "THURSDAY",
    4: "FRIDAY",
    5: "SATURDAY",
    6: "SUNDAY"
}

# This class handles the editing of an outlet json file
class OutletManager():

    def __init__(self):
        self.outlet_list = self.load_outlets()

    # Reads outlets json file and returns a dictionary
    def load_outlets(self):
        with open(OUTLETS_FILE, "r") as outlets:
            return json.loads(outlets.read())

    # Writes contents of outlet list to outlet json file
    def save_outlets(self):
        with open(OUTLETS_FILE, "w") as outlets:
            outlets.write(json.dumps(self.outlet_list))

    # Updates outlet values
    # If outlet doesn't exist it creates a new
    def update_outlet(self, new_outlet : dict()):

        print(f"Updating outlet: {new_outlet['id']} {new_outlet['name']}")

        doesExist = False

        for i in range(0, len(self.outlet_list)):
            if self.outlet_list[i]["id"] == new_outlet["id"]:
                self.outlet_list[i] = new_outlet
                doesExist = True

        if not doesExist:
            self.outlet_list.append(new_outlet)

    # Checks all outlet triggers and determines
    # if outlet should be on or not
    # Returns outlets in a parsed format
    def check_triggers(self, record):

        for out in self.outlet_list:
            if out['stay_on'] is False:
                trigger_counter = 0
                for trigger in out['triggers']:
                    if trigger['type'] == 'TIME':
                        trigger_counter = trigger_counter + self.check_time_trigger(trigger)
                    elif trigger['type'] == 'CONDITION':
                        trigger_counter = trigger_counter + self.check_condition_trigger(trigger, record)

                out['is_on'] = trigger_counter > 0
            else:
                out['is_on'] = True

        self.save_outlets()
        return self.parse_outlets()

    # Checks if time trigger condition is true
    def check_time_trigger(self, trigger):

        trigger_time = datetime.strptime(trigger['time'], '%H:%M').time()
        end_time = self.add_minutes(trigger_time, trigger['duration'])
        current_time = datetime.now().time()
        current_weekday = WEEKDAYS[datetime.today().weekday()]

        if trigger['weekday'] == "EVERYDAY" or trigger['weekday'] == current_weekday:
            if current_time >= trigger_time and current_time < end_time:
                return True
        
        return False

    # Adds given minutes to a given datetime object
    def add_minutes(self, time, minutes):
        secs = minutes * 60
        fulldate = datetime(100, 1, 1, time.hour, time.minute, time.second)
        fulldate = fulldate + timedelta(seconds=secs)
        return fulldate.time()

    # Checks if condition trigger condition is true
    def check_condition_trigger(self, trigger, record):
                
        record_value = self.get_record_value(trigger, record)

        if not record_value:
            return False

        if trigger['operation'] == 'LOWER':
            return record_value < trigger['value']
        elif trigger['operation'] == 'EQUALS':
            return record_value == trigger['value']
        elif trigger['operation'] == 'GREATER':
            return record_value > trigger['value']
        elif trigger['operation'] == 'NOT':
            return record_value != trigger['value']
        
        return False

    # Returns sensor value using target from a trigger
    def get_record_value(self, trigger, record):

        if trigger['target'] != 'NO_SENSOR':
            if trigger['target'] == 'AIR_TEMP':
                return record['air_temperature']
            elif trigger['target'] == 'AIR_PRES':
                return record['air_pressure']

            return record[trigger['target'].lower()] 

        return False

    # Creates a json array from the outlet list
    # Parses the outlet info so there is only
    # Id, Name and Is_on values
    def parse_outlets(self):

        parsed_outlets = []

        for out in self.outlet_list:
            copy_outlet = {}
            copy_outlet['id'] = out['id']
            copy_outlet['name'] = out['name']
            copy_outlet['is_on'] = out['is_on']
            parsed_outlets.append(copy_outlet)
        
        return parsed_outlets


