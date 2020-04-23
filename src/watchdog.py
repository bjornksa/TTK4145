import threading
import time

class Watchdog():
    # Constant limiting how long a watchdog is kept alive. Seconds.
    TIMEOUT = 20

    def __init__(self, callback):
        self.callback = callback
        # List of orders pushed to the watchdog. Each element on the form {id, floor, button, timestamp}.
        self.list = []

    # Watchdog interface
    def add_watchdog(self, id, floor, button):
        timestamp = int(time.time())
        watchdog = {'id': id, 'floor': floor, 'button': button, 'timestamp': timestamp}
        self.list.append(watchdog)

    def clear_watchdog(self, id, floor):
        self.list[:] = [watchdog for watchdog in self.list if not (watchdog['id'] == id and watchdog['floor'] == floor)]

    # Running the watchdog
    def _watchdog_main(self, callback, t):
        while True:
            # If time exceeds watchdog+timeout, then send out a new order
            current_time = int(time.time())
            for watchdog in self.list:
                if watchdog['timestamp'] + Watchdog.TIMEOUT < current_time:
                    #print('WATCHDOG TIMEOUT')
                    if watchdog['button'] == 2: # Cab order
                        callback({'type': 'broadcast_order', 'floor': watchdog['floor'], 'button': watchdog['button'], 'order_elevator_id': watchdog['id']})
                    else:
                        callback({'type': 'broadcast_cost_request', 'floor': watchdog['floor'], 'button': watchdog['button']})
                    self.clear_watchdog(watchdog['id'], watchdog['floor'])
            time.sleep(1)

    def run(self):
        main_thread = threading.Thread(target=self._watchdog_main, args=(self.callback, 1))
        main_thread.start()
