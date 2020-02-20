import ctypes
import threading
import time

testlib = ctypes.CDLL('/home/simen/Documents/school/sanntidsprogrammering/TTK4145/wrapper_tester/test.so')

def notification_tester(name, t):
    while True:
        count = testlib.simple_timer(t)
        print(f'Timer {name} firing, count: {count}!!!')

def main_tester():
    testlib.main()

if __name__ == '__main__':
    x = threading.Thread(target=notification_tester, args=('simens tråd', 1))
    y = threading.Thread(target=notification_tester, args=('Erlends tråd', 4))
    main_thread = threading.Thread(target=main_tester)
    main_thread.start()
    x.start()
    y.start()
    main_thread.join()
    x.join()
    y.join()
