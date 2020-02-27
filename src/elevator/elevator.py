import ctypes
import threading
import time
import subprocess
import os

testlib = ctypes.CDLL(os.path.dirname(__file__) + 'elev_algo/ttk4145demoelevator.so')

def notification_tester(name, t):
    while True:
        testlib.lamp(1)
        print(f'Timer {name} firing, count:!!')
        time.sleep(5)
        testlib.lamp(0)
        time.sleep(5)

def main_tester():
    testlib.main()

if __name__ == '__main__':
    x = threading.Thread(target=notification_tester, args=('simens tråd', 1))
    #y = threading.Thread(target=notification_tester, args=('Erlends tråd', 4))

    #main_tester()


    main_thread = threading.Thread(target=main_tester)
    main_thread.start()
    x.start()
    #
    main_thread.join()
    x.join()
