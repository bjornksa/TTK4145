import threading
import time
from collections import namedtuple

# Constant limiting how long a watchdog is kept alive. Seconds.
TIMEOUT = 30

# List of orders pushed to the watchdog. Each element on the form [Order, timestamp]
list = []

# Watchdog interface
def add_watchdog(ip, floor, button):
    timestamp = int(time.time())
    watchdog = [ip, floor, button, timestamp]
    list.append(watchdog)

def clear_watchdog(ip, floor):
    list[:] = [watchdog for watchdog in list if not (watchdog[0] == ip and watchdig[1] == floor)]

# Running the watchdog
def watchdog_main(callback, t):
    while True:
        # If time exceeds watchdog+timeout, then send out a new order
        current_time = int(time.time())
        for watchdog in list:
            timestamp = watchdog[1]
            if timestamp + TIMEOUT < current_time:
                callback({'type': 'broadcast_order', 'floor': watchdog[0].floor, 'button': watchdog[0].button})
                clear_watchdog(watchdog[0])
        time.sleep(1)

def run(callback):
    print("Watchdog running")
    main_thread = threading.Thread(target=watchdog_main, args=(callback, 1))
    main_thread.start()
