import threading
import time
from collections import namedtuple

# Constant limiting how long a watchdog is kept alive. Seconds.
timeout = 30

# Order type
Order = namedtuple('Order', 'ip floor button')

# List of orders pushed to the watchdog. Each element on the form [Order, timestamp]
list = []

# Watchdog interface
def add_watchdog(order):
    timestamp = int(time.time())
    watchdog = [order, timestamp]
    list.append(watchdog)

def clear_watchdog(order):
    list[:] = [watchdog for watchdog in list if not watchdog[0] == order]

# Function to talk to the distributor
def new_order(floor, button):
    # send something to distributor
    print(f'watchdog expired, new order {floor}, {button}')

# Running the watchdog
def watchdog_main():
    while True:
        # If time exceeds watchdog+timeout, then send out a new order
        current_time = int(time.time())
        for watchdog in list:
            timestamp = watchdog[1]
            if timestamp + timeout < current_time:
                new_order(watchdog[0].floor, watchdog[0].button)
                clear_watchdog(watchdog[0])
        time.sleep(1)

if __name__ == '__main__':
    main_thread = threading.Thread(target=watchdog_main)
    main_thread.start()
    main_thread.join()
