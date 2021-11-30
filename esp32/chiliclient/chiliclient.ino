#include "chiliclient.h"
#include "outletmgr.h"

Adafruit_BME280 bme;

/*
 * SSID 
 */
const char* ssid = "";

/*
 * WiFi password 
 */
const char* pass = "";

/*
 * Server ip address
 * 192.168.5.201
 */
const char* host = "192.168.5.201";

/*
 * Server port
 */
const int port = 8080;

/*
 * HttpClient timeout time
 */
const long clientTimeout = 20000;

/*
 * Server address as a string
 */
std::string hostaddress = "";

/*
 * Path for the POST request
 */
std::string resource = "/post-record";

/*
 * HttpClient instance
 */
HTTPClient http;

/*
 * Pin number for the light value reading
 */
const int lightPin = 34;

/*
 * Starts listening Serial
 * Builds the whole address for the POST request as string
 * Checks if BME sensor can be found. If not then it does not continue.
 * Sets pin mode for lightPin
 * Connects to Wifi
 */
void setup() {
  Serial.begin(115200);

  hostaddress = create_hostaddress();

  Serial.println("Initializing outlets...");
  init_outlets();

  Serial.println("Searching BME280...");
  if(!bme.begin(0x76))
  {
    Serial.println("Could not find BME280, check wiring!");
    while(1);  
  }
  Serial.println("BME280 found.");

  Serial.println("Initializing light pin...");
  pinMode(lightPin, INPUT);

  Serial.println("Connecting to Wifi...");
  WiFi.begin(ssid, pass);
  
}

/*
 * Reads sensor values and converts them to a json format.
 * Sends json data to the server
 * Checks status of every outlet
 */
void loop() {

  Serial.println("Reading sensor values...");
  SensorValues values = read_sensor_values();
  DynamicJsonDocument jsonDoc = values_to_json(values);
  send_data(jsonDoc);
  check_outlets();

  delay(SLEEP_TIME);
}

/*
 * Reads air temparature, air pressure and humidity from the 
 * BME sensor. Reads light value from the light sensor.
 * Returns sensor values as a struct
 */
SensorValues read_sensor_values()
{
  SensorValues values;
  // Celsius
  values.air_temperature = round_value(bme.readTemperature());
  // hPa
  values.air_pressure = round_value(bme.readPressure() / 100.0F);
  // Percent
  values.humidity = round_value(bme.readHumidity());
  values.light = analogRead(lightPin);
  
  return values;
}

/*
 * Takes json document as a parameter.
 * If it is connected to a Wifi then it sends
 * a POST request to the server.
 * Server sends outlet info as a response.
 * Outlet info is in json format. 
 * Updates outlets according to response json
 */
void send_data(DynamicJsonDocument jsonDoc)
{
  if(WiFi.status() == WL_CONNECTED)
  {
      Serial.println("Wifi is connected");
      Serial.println("Sending POST request to the server...");
      http.begin(hostaddress.c_str());
      http.setTimeout(clientTimeout);
      http.addHeader("Content-Type", "application/json");

      std::string str_json = "";
      serializeJson(jsonDoc, str_json);
      int httpCode = http.POST(str_json.c_str());

      if(httpCode > 0)
      {
        if(httpCode == HTTP_CODE_OK)
        {
          Serial.println("[HTTP] POST sent successfully!");
          
          String response = http.getString();
          char str_response[response.length()];
          strcpy(str_response, response.c_str());

          Serial.println(response.c_str());

          DynamicJsonDocument responseJsonDoc(1024);
          deserializeJson(responseJsonDoc, str_response);
          
          update_outlet_list(responseJsonDoc);
        }
        else
      {
        Serial.printf("[HTTP] POST failed, error: %s \n", http.errorToString(httpCode).c_str());
        }
      }
      else
      {
        Serial.printf("[HTTP] POST failed, error: %s \n", http.errorToString(httpCode).c_str());
      }

      http.end();
      
  }  
}

void get_startup_config()
{
  if(Wifi.status() == WL_CONNECTED)
  {
    Serial.println("Wifi is connected.");
    Serial.println("Requesting startup config from server");
  }
}

/*
 * Converts sensor values to a json
 * Returns a json document
 */
DynamicJsonDocument values_to_json(SensorValues values)
{
  DynamicJsonDocument jsonDoc(1024);
  jsonDoc["air_temperature"] = values.air_temperature;
  jsonDoc["air_pressure"] = values.air_pressure;
  jsonDoc["humidity"] = values.humidity;
  jsonDoc["light"] = values.light;

  return jsonDoc;
}

/*
 * Rounds a float value to two decimal places
 */
float round_value(float value)
{
  return floorf(value * 100) / 100;  
}

/*
 * Converts a float to a string
 */
std::string convert_to_string(float value, int decimals)
{
  char buff[10];
  dtostrf(value, 4, decimals, buff);
  std::string str = cstr_to_string(buff, arr_len(buff));
  return str;
}

/*
 * Converts an int to a string
 */
std::string convert_to_string(int value)
{
  char buff[10];
  dtostrf(value, 4, 0, buff);
  std::string str = cstr_to_string(buff, arr_len(buff));
  return str;
}

/*
 * Converts a C-string to a string
 */
std::string cstr_to_string(char* cstr, int cstr_size)
{
  std::string str = "";
  for(int i = 0; i < cstr_size; i++)
  {
    str += cstr[i];
  }
  return str;
}

/*
 * Counts a length of a char array
 */
int arr_len(char arr[])
{
  int counter = 0;
  char* p = arr;
  while(*p != '\0')
  {
    *p++;
    counter++;
  }
  return counter;
}

/*
 * Removes all whitespaces from the left side of a string
 */
void ltrim(std::string& str, const std::string& trim_chars)
{
  std::string::size_type pos = str.find_first_not_of(trim_chars);
  str.erase(0, pos);
}

/*
 * Creates string that contains the whole address to the server
 */
string create_hostaddress()
{
  string tmpAddr = "http://" + cstr_to_string((char*)host, arr_len((char*)host)) + ":";
  tmpAddr += convert_to_string(port);
  tmpAddr += resource;
  return tmpAddr;
}
