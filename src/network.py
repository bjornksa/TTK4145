import json  #parse = loads(), serialize = dumps()
import socket
from time import sleep
import time
import threading
import ast

BROADCAST_IP = "255.255.255.255"
BROADCAST_PORT = 1440
PRIVATE_PORT = 1560

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
MY_IP = s.getsockname()[0]
s.close()

elevators = [] # {elevator_id, ip, socket, timestamp}

def send(elevator_id, data):
    '''
    elevator = next((elev for elev in elevators if elev['elevator_id' == elevator_id), None)
    s = elevator['socket']
    s.sendall(data)
    s.close()
    print('Received', repr(data))
    '''
    pass

# Den her gjør om data fra melding til task og så kjører den callback()-funksjonen fra distributor
def callback_wrapper(data, callback):
    callback_data = data
    if data['type'] == 'cost_request':
        callback_data['type'] = 'get_cost'

    elif data['type'] == 'order':
        callback_data['type'] = 'add_order_or_watchdog'

    elif data['type'] == 'clear_order':
        callback_data['type'] = 'clear_order'

    elif data['type'] == 'cost':
        callback_data['type'] = 'receive_cost'

    elif data['type'] == 'acknowledge_order':
        callback_data['type'] = 'acknowledge_order'

    callback(callback_data)


# Running the network listeners
def listener_private(callback, t):
    receive_private_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_private_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receive_private_socket.bind(("", PRIVATE_PORT))

    while True:
        data = receive(receive_private_socket)
        #print("received private: ", data)
        callback_wrapper(data, callback)
        sleep(0.01)

def receive(sock):
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data = ast.literal_eval(data.decode('utf-8'))
    return data

def keep_track_of_elevators(my_id):
    receive_broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receive_broadcast_socket.bind(("", BROADCAST_PORT))

    while True:
        data = receive(receive_broadcast_socket)
        elevator = next((elevator for elevator in elevators if elevator['elevator_id'] == data['elevator_id']), None)
        if elevator is not None:
            elevator['timestamp'] = int(time.time())
        else:
            print('open socket')
            if my_id > data['elevator_id']:
                # Server
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((data['ip'], PRIVATE_PORT))
                s.listen(1)
                conn, addr = s.accept()
                print(f'Connection address: {addr}')
                elevators.append({'elevator_id': data['elevator_id'], 'ip': data['ip'], 'socket': conn, 'timestamp': int(time.time())})
            else:
                # Client or drop from list

        elevators_new = []
        for elevator in elevators:
            if elevator['timestamp'] + 10 < int(time.time()):
                print('close socket')
            else:
                elevators_new.append(elevator)
        elevators[:] = elevators_new
        sleep(0.01)

def broadcast_alive_signal(my_id, t):
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        data = {'elevator_id': my_id, 'ip': MY_IP}
        data_string = json.dumps(data)
        s.sendto(data_string.encode(), (BROADCAST_IP, BROADCAST_PORT))
        s.close()
        sleep(5)

def run(elevator_id, callback):
    broadcast_alive_signal_thread = threading.Thread(target=broadcast_alive_signal, args=(elevator_id, 1))
    broadcast_alive_signal_thread.start()

    keep_track_of_elevators_thread = threading.Thread(target=keep_track_of_elevators, args=(elevator_id, 1))
    keep_track_of_elevators_thread.start()

run(1, False)
