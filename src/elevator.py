import ctypes
import threading
import time
import subprocess
import os
import queue

# Make elev_algo callable from Python
elevatorlib = ctypes.CDLL(os.path.dirname(__file__) + '/elev_algo/ttk4145demoelevator.so')

# Initialize C callback queue
callbackQueue = queue.Queue(maxsize=0)

# Wrappers for C functions in elev_algo
def set_lamp(floor, button):
    elevatorlib.set_lamp(floor, button)

def clear_lamps(floor):
    for i in range(0,3):
        elevatorlib.clear_lamp(floor, i)

def get_cost(floor, button):
    return elevatorlib.get_cost(floor, button)

def add_order(floor, button):
    elevatorlib.add_order(floor, button)
    set_lamp(floor, button)

# Functions supposed to be callable from elev_algo
def new_order(floor, button):
    if button == 2: # Cab order
        callbackQueue.put({'type': 'broadcast_order', 'floor': floor, 'button': button, 'order_elevator_id': 'MY_ID'})
    else:
        callbackQueue.put({'type': 'broadcast_cost_request', 'floor': floor, 'button': button})

def finished_order(floor):
    callbackQueue.put({'type': 'broadcast_finished_order', 'floor': floor})

# Make the above functions callable from c as callback functions
c_new_order = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)(new_order)
c_finished_order = ctypes.CFUNCTYPE(None, ctypes.c_int)(finished_order)

# Running the elevator
def elevator_runner(port_offset, t):
    c_port_offset = ctypes.c_int(int(port_offset))
    elevatorlib.run(c_port_offset, c_new_order, c_finished_order)

def elevator_callback_listener(callback, t):
    while True:
        callbackElement = callbackQueue.get(True)
        callback(callbackElement)

def run(elevator_id, callback):
    elevator_runner_thread = threading.Thread(target=elevator_runner, args=(elevator_id, 1))
    elevator_callback_listener_thread = threading.Thread(target=elevator_callback_listener, args=(callback, 1))

    elevator_runner_thread.start()
    elevator_callback_listener_thread.start()
