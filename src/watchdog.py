import threading
import time

# Constant limiting how long a watchdog is kept alive. Seconds.
TIMEOUT = 30

# List of orders pushed to the watchdog. Each element on the form [Order, timestamp]
list = []

# Watchdog interface
def add_watchdog(id, floor, button):
    timestamp = int(time.time())
    watchdog = {'id': id, 'floor': floor, 'button': button, 'timestamp': timestamp}
    list.append(watchdog)

def clear_watchdog(id, floor):
    list[:] = [watchdog for watchdog in list if not (watchdog['id'] == id and watchdog['floor'] == floor)]

# Running the watchdog
def watchdog_main(callback, t):
    while True:
        # If time exceeds watchdog+timeout, then send out a new order
        current_time = int(time.time())
        for watchdog in list:
            if watchdog['timestamp'] + TIMEOUT < current_time:
                #print('WATCHDOG TIMEOUT')
                if watchdog['button'] == 2: # Cab order
                    callback({'type': 'broadcast_order', 'floor': watchdog['floor'], 'button': watchdog['button'], 'order_elevator_id': watchdog['id']})
                else:
                    callback({'type': 'broadcast_cost_request', 'floor': watchdog['floor'], 'button': watchdog['button']})
                clear_watchdog(watchdog['id'], watchdog['floor'])
        time.sleep(1)

def run(callback):
    main_thread = threading.Thread(target=watchdog_main, args=(callback, 1))
    main_thread.start()
