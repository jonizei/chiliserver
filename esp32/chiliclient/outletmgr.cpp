#include "chiliclient.h"
#include "outletmgr.h"

/*
 * Count of the outlets
 */
const int outlet_count = 3;

/*
 * Array of outlets
 */
Outlet outlet_list[outlet_count];

/*
 * Initializes all the outlets and
 * adds them to the array of outlets.
 * Then initializes the pins of the outlets.
 */
void init_outlets()
{
  Outlet outlet1;
  outlet1.id = 1;
  outlet1.name = "Outlet_1";
  outlet1.pin = 27;
  outlet1.is_reverse = true;

  Outlet outlet2;
  outlet2.id = 2;
  outlet2.name = "Outlet_2";
  outlet2.pin = 14;
  outlet2.is_reverse = true;

  Outlet outlet3;
  outlet3.id = 3;
  outlet3.name = "Outlet_3";
  outlet3.pin = 26;
  outlet3.is_reverse = false;

  outlet_list[0] = outlet1;
  outlet_list[1] = outlet2;
  outlet_list[2] = outlet3;

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




  
