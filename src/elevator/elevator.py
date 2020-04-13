import ctypes
import threading
import time
import subprocess
import os

elevatorlib = ctypes.CDLL(os.path.dirname(__file__) + 'elev_algo/ttk4145demoelevator.so')

def set_lamp(floor, button):
    elevatorlib.set_lamp(floor, button)

def clear_lamp(floor, button):
    elevatorlib.clear_lamp(floor, button)

def get_cost(floor, button):
    return elevatorlib.get_cost(floor, button)

def add_order(floor, button):
    elevatorlib.add_order(floor, button)

def elevator_test():
    while True:
        #print(f'Timer firing')
        #elevatorlib.add_order(1,1)
        #time.sleep(5)
        #elevatorlib.add_order(3,2)
        #time.sleep(5)
        set_lamp(2,2)
        time.sleep(3)
        clear_lamp(2,2)
        time.sleep(3)
        cost = get_cost(3,1)
        print(f'Cost {cost}')
        time.sleep(3)
        add_order(1,1)
        time.sleep(5)
        add_order(3,2)

def elevator_main():
    elevatorlib.mainish()

if __name__ == '__main__':
    main_thread = threading.Thread(target=elevator_main)
    test_thread = threading.Thread(target=elevator_test)

    main_thread.start()
    test_thread.start()

    main_thread.join()
    test_thread.join()
