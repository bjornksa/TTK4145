#pragma once

#include "elevator_io_types.h"
#include "elevator.h"

void fsm_set_finished_order_at_idle_flag();
void fsm_clear_finished_order_at_idle_flag();
int fsm_check_finished_order_at_idle_flag();

void fsm_onInitBetweenFloors(void);
void fsm_onRequestButtonPress(int btn_floor, Button btn_type);
void fsm_onFloorArrival(int newFloor, void* finished_order(int));
void fsm_onDoorTimeout(void);
Elevator fsm_getElevator();
