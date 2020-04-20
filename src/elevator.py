import ctypes
import threading
import time
import subprocess
import os
import queue
# Make elev_algo callable from Python
elevatorlib = ctypes.CDLL(os.path.dirname(__file__) + '/elev_algo/ttk4145demoelevator.so')

class Elevator():
    def __init__(self, elevator_id, callback):
        self.elevator_id = elevator_id
        self.callback = callback
        # Initialize C callback queue
        self.callbackQueue = queue.Queue(maxsize=0)
        # Make private functions callable from c as callback functions
        self.c_new_order = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)(self._new_order)
        self.c_finished_order = ctypes.CFUNCTYPE(None, ctypes.c_int)(self._finished_order)

    # Interface aka wrappers for C functions in elev_algo
    def set_lamp(self, floor, button):
        elevatorlib.set_lamp(floor, button)

    def clear_lamps(self, floor):
        for i in range(0,3):
            elevatorlib.clear_lamp(floor, i)

    def get_cost(self, floor, button):
        return elevatorlib.get_cost(floor, button)

    def add_order(self, floor, button):
        elevatorlib.add_order(floor, button)
        self.set_lamp(floor, button)

    # Functions supposed to be callable from elev_algo
    def _new_order(self, floor, button):
        if button == 2: # Cab order
            self.callbackQueue.put({'type': 'broadcast_order', 'floor': floor, 'button': button, 'order_elevator_id': 'MY_ID'})
        else:
            self.callbackQueue.put({'type': 'broadcast_cost_request', 'floor': floor, 'button': button})

    def _finished_order(self, floor):
        self.callbackQueue.put({'type': 'broadcast_finished_order', 'floor': floor})

    # Running the elevator
    def _elevator_runner(self, port_offset, t):
        c_port_offset = ctypes.c_int(int(port_offset))
        elevatorlib.run(c_port_offset, self.c_new_order, self.c_finished_order)

    def _elevator_callback_listener(self, callback, t):
        while True:
            callbackElement = self.callbackQueue.get(True)
            callback(callbackElement)

    def run(self):
        elevator_runner_thread = threading.Thread(target=self._elevator_runner, args=(self.elevator_id, 1))
        elevator_callback_listener_thread = threading.Thread(target=self._elevator_callback_listener, args=(self.callback, 1))

        elevator_runner_thread.start()
        elevator_callback_listener_thread.start()
