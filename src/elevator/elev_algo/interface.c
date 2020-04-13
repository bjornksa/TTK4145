#include "mainish.h"
#include "driver/elevator_hardware.h"

void start() {
  mainish();
}

void set_lamp(int floor, int button) {
  elevator_hardware_set_button_lamp(button, floor, 1);
}

void clear_lamp(int floor, int button) {
  elevator_hardware_set_button_lamp(button, floor, 0);
}

int get_cost(int floor, int button) {
  return 0;
}

void add_order(int floor, int button) {

}
