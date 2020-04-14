#include "elevator_hardware.h"

int main() {
    elevator_hardware_init(0);

    while(1) {
	elevator_hardware_set_motor_direction(DIRN_DOWN);
	while(elevator_hardware_get_floor_sensor_signal() != 0) {}
	elevator_hardware_set_motor_direction(DIRN_UP);
	while(elevator_hardware_get_floor_sensor_signal() != 3) {}
    }
}
