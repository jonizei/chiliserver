#ifndef OUTLETMGR_H
#define OUTLETMGR_H

/*
 * Default struct of an outlet
 */
struct Outlet {
  int id = 0;
  std::string name = "";
  bool is_on = false;
  int pin = 0;
  bool is_reverse = false;
};

void add_outlet(std::string, int, bool);
void init_outlets();
void check_outlets();
void init_outlet_pins();
void update_outlet_list(DynamicJsonDocument);

#endif
