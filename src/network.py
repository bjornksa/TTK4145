import json  #parse = loads(), serialize = dumps()
import socket
from time import sleep
import threading
import ast

BROADCAST_IP = "255.255.255.255"
BROADCAST_PORT = 1440
PRIVATE_PORT = 1560

def send(ip, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data_string = json.dumps(data)
    s.sendto(data_string.encode(), (ip, PRIVATE_PORT))
    s.close()

def broadcast(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    data_string = json.dumps(data)
    s.sendto(data_string.encode(), (BROADCAST_IP, BROADCAST_PORT))
    s.close()

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

def receive(sock):
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data = ast.literal_eval(data.decode('utf-8'))
    return data

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

def listener_broadcast(callback, t):
    receive_broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receive_broadcast_socket.bind(("", BROADCAST_PORT))

    while True:
        data = receive(receive_broadcast_socket)
        #print("received broadcast: ", data)
        callback_wrapper(data, callback)
        sleep(0.01)

# Denne kalles opp fra distributor for å dra igang nettverkslytting.
# callback() er en funksjon i distributor som skal kalles opp når vi har mottatt en melding
def run(callback):
    listener_private_thread = threading.Thread(target=listener_private, args=(callback, 1))
    listener_broadcast_thread = threading.Thread(target=listener_broadcast, args=(callback, 1))
    listener_private_thread.start()
    listener_broadcast_thread.start()
