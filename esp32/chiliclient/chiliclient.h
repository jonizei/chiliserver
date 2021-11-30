#ifndef CHILICLIENT_H
#define CHILICLIENT_H

#include <WiFi.h>
#include <HTTPClient.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <Adafruit_BME280.h>
#include <ArduinoJson.h>
#include <map>

/*
 * Delay time between readings
 */
#define SLEEP_TIME 60000

struct SensorValues {
  float air_temperature;
  float air_pressure;
  float humidity;
  int light;  
};

/*
 * White space characters
 */
const std::string white_spaces(" \f\n\r\t\v");

void send_data(DynamicJsonDocument);
SensorValues read_sensor_data();
DynamicJsonDocument values_to_json(SensorValues);
std::string cstr_to_string(char*, int);
int arr_len(char[]);
std::string convert_to_string(float);
std::string convert_to_string(int);
void ltrim(std::string&, const std::string& trim_values = white_spaces);
float round_value(float);
string create_hostaddress();

#endif
