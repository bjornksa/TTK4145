#include "mainish.h"
#include "driver/elevator_hardware.h"
#include "elevator.h"
#include "fsm.h"
#include "requests.h"

#define TRAVEL_TIME 2
#define DOOR_OPEN_TIME 3

void run(int portOffset, void* new_order(int, int), void* finished_order(int)) {
  mainish(portOffset, new_order, finished_order);
}

void set_lamp(int floor, int button) {
  elevator_hardware_set_button_lamp(button, floor, 1);
}

void clear_lamp(int floor, int button) {
  elevator_hardware_set_button_lamp(button, floor, 0);
}

int get_cost(int floor, int button) {
  Elevator e_old = fsm_getElevator();
  Button b = button;
  int f = floor;
  Elevator e = e_old;
  e.requests[f][b] = 1;

  int arrivedAtRequest = 0;
  void ifEqual(Button inner_b, int inner_f){
    if(inner_b == b && inner_f == f){
      arrivedAtRequest = 1;
    }
  }

  int duration = 0;

  switch(e.behaviour){
  case EB_Idle:
    e.dirn = requests_chooseDirection(e);
    if(e.dirn == D_Stop){
      return duration;
    }
    break;
  case EB_Moving:
    duration += TRAVEL_TIME/2;
    e.floor += e.dirn;
    break;
  case EB_DoorOpen:
    duration -= DOOR_OPEN_TIME/2;
  }


  while(1){
    if(requests_shouldStop(e)){
      e = requests_interface_clearAtCurrentFloor(e, ifEqual);
      if(arrivedAtRequest){
        return duration;
      }
      duration += DOOR_OPEN_TIME;
      e.dirn = requests_chooseDirection(e);
    }
    e.floor += e.dirn;
    duration += TRAVEL_TIME;
  }
  return duration;
}

void add_order(int floor, int button) {
  Button btn = button;
  fsm_onRequestButtonPress(floor, btn);
}
