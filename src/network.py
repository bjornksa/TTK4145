import json  #parse = loads(), serialize = dumps()
import socket
from time import sleep
import threading
import ast

BROADCAST_IP = "255.255.255.255"
SENDER_IP = socket.gethostname()
BROADCAST_PORT = 1440
PRIVATE_PORT = 1560

def send(ip, type, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = {
        "type": type,
        "sender_ip": SENDER_IP,
        "data": data
    }
    message_string = json.dumps(message)
    s.sendto(message_string.encode(), (ip, PRIVATE_PORT))
    s.close()

def broadcast(type, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = {
        "type": type,
        "sender_ip": SENDER_IP,
        "data": data
    }
    message_string = json.dumps(message)
    s.sendto(message_string.encode(), (BROADCAST_IP, BROADCAST_PORT))
    s.close()

def callback_wrapper(data, callback):
    data = ast.literal_eval(data.decode('utf-8'))
    print(data)
    if data['type'] == 'cost_request':
        callback_data = {'type':     'get_cost',
                        'sender_ip': data['sender_ip'],
                        'floor':     data['data']['floor'],
                        'button':    data['data']['button']
                        }

    elif data['type'] == 'order':
        callback_data = {'type':    'add_order_or_watchdog',
                        'order_ip': data['data']['order_ip'],
                        'floor':    data['data']['floor'],
                        'button':   data['data']['button']
                        }

    elif data['type'] == 'clear_order':
        callback_data = {'type':    'clear_order',
                        'order_ip': data['data']['ip'],
                        'floor':    data['data']['floor']
                        }

    elif data['type'] == 'cost':
        callback_data = {'type':  'receive_cost',
                        'cost':   data['data']['cost'],
                        'floor':  data['data']['floor'],
                        'button': data['data']['button']
                        }

    elif data['type'] == 'order_acknowledge':
        callback_data = {'type':  'acknowledge_order',
                        'floor':  data['data']['floor'],
                        'button': data['data']['button']
                        }

    callback(callback_data)


def receive(sock):
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    return data

# Running the network listeners
def listener_private(callback, t):
    receive_private_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_private_socket.bind(("", PRIVATE_PORT))

    while True:
        data = receive(receive_private_socket)
        print("received private: ", data)
        callback_wrapper(data, callback)
        sleep(0.5)

def listener_broadcast(callback, t):
    receive_broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_broadcast_socket.bind(("", BROADCAST_PORT))

    while True:
        data = receive(receive_broadcast_socket)
        print("received broadcast: ", data)
        callback_wrapper(data, callback)
        sleep(0.5)

def run(callback):
    print("Network running")
    listener_private_thread = threading.Thread(target=listener_private, args=(callback, 1))
    listener_broadcast_thread = threading.Thread(target=listener_broadcast, args=(callback, 1))
    listener_private_thread.start()
    listener_broadcast_thread.start()
