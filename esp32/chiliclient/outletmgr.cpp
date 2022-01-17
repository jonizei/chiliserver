#include "chiliclient.h"
#include "outletmgr.h"

/**
 * Outlet capacity
 */
const int MAX_OUTLET = 3;

/*
 * Count of the outlets
 */
int outlet_count = 0;

/*
 * Array of outlets
 */
Outlet outlet_list[MAX_OUTLET];

/**
 * Initializes new outlet and adds it to the outlet array
 * Requires name of the outlet, number of the pin controlling the outlet
 * and boolean which tells if relay turns on either LOW or HIGH signal
 */
void add_outlet(std::string name, int pin, bool is_reverse)
{
  Outlet outlet;
  outlet.id = outlet_count;
  outlet.name = name;
  outlet.pin = pin;
  outlet.is_reverse = is_reverse;
  
  if(outlet_count > -1 && outlet_count < MAX_OUTLET)
  {
    outlet_list[outlet_count] = outlet;
    outlet_count++;
  }
}

/*
 * Initializes all the outlets and
 * adds them to the array of outlets.
 * Then initializes the pins of the outlets.
 */
void init_outlets()
{
  add_outlet("Outlet_1", 27, true);
  add_outlet("Outlet_2", 14, true);
  add_outlet("Outlet_3", 26, false);

  init_outlet_pins();
}

/*
 * Sets all outlets pin as OUTPUT pins
 */
void init_outlet_pins()
{
  for(int i = 0; i < outlet_count; i++)
  {
    if(outlet_list[i].pin > 0)
    {
      pinMode(outlet_list[i].pin, OUTPUT);
    }
  }
}

/*
 * Checks all outlets if any of them is set to on or off.
 * Some relays works that HIGH is on and LOW is off and 
 * some works the other way around.
 * Is_reverse determines how the relay works.
 */
void check_outlets()
{
  for(int i = 0; i < outlet_count; i++)
  {
    if(outlet_list[i].pin > 0)
    {
      if(outlet_list[i].is_on)
      {
        if(outlet_list[i].is_reverse)
        {
          digitalWrite(outlet_list[i].pin, LOW);
        }
        else
        {
          digitalWrite(outlet_list[i].pin, HIGH);
        }
      }
      else
      {
        if(outlet_list[i].is_reverse)
        {
          digitalWrite(outlet_list[i].pin, HIGH);
        }
        else
        {
          digitalWrite(outlet_list[i].pin, LOW);
        }
      }  
    }
  }
}

/*
 * Takes json document as a parameter.
 * Tries to find outlet with the same id
 * and then copies the data from the json document.
 */
void update_outlet_list(DynamicJsonDocument jsonDoc)
{
  
  for(int i = 0; i < outlet_count; i++)
  {
    for(int j = 0; j < jsonDoc.size(); j++)
    {
      JsonObject jsonObject = jsonDoc[j];
      
      if(jsonObject["id"] == outlet_list[i].id)
      {
        outlet_list[i].is_on = jsonObject["is_on"];
      }
      
    }
  }
}




  
