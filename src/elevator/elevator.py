import ctypes
import threading
import time
import subprocess
import os

elevatorlib = ctypes.CDLL(os.path.dirname(__file__) + 'elev_algo/ttk4145demoelevator.so')

def elevator_test():
    while True:
        print(f'Timer firing')
        elevatorlib.add_order(1,1)
        time.sleep(5)
        elevatorlib.add_order(3,2)
        time.sleep(5)

def elevator_main():
    elevatorlib.mainish()

if __name__ == '__main__':
    main_thread = threading.Thread(target=elevator_main)
    test_thread = threading.Thread(target=elevator_test)

    main_thread.start()
    test_thread.start()

    main_thread.join()
    test_thread.join()
