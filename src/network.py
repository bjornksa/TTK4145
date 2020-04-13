import json  #parse = loads(), serialize = dumps()
import socket

from time import sleep

SENDER_IP = socket.gethostname()
BROADCAST_PORT = 1440
PRIVATE_PORT = 1560

def send(type, data, ip):
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
    s.sendto(message_string.encode(), ("255.255.255.255", BROADCAST_PORT))
    s.close()

if __name__ == "__main__":
    order = {
        "ip": "192.168",
        "floor": 2,
        "button": 1
    }
    while True:
        send("cost_request", order, "10.2.192.2")
        print("sent", json.dumps(order))
        sleep(1)
