import json  #parse = loads(), serialize = dumps()
import socket

from time import sleep

SENDER_IP = socket.gethostname()
BROADCAST_PORT = 1440
PRIVATE_PORT = 1560


def send(type, response, ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = {
        "messagetype": type,
        "sender_ip": SENDER_IP,
        "response": response
    }
    s.sendto(json.dumps(message), (ip, PRIVATE_PORT))
    s.close()


def broadcast(type, order):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = {"messagetype": type,"sender_ip": SENDER_IP, "order": order    }
    message_string = json.dumps(message)
    s.sendto(message_string.encode(), ("255.255.255.255", BROADCAST_PORT))
    s.close()


if __name__ == "__main__":
    order = {
        "elevator":1,
        "elevator_ip": "192.168",
        "order_floor": 2,
        "order_type":"internal",
        "order_dir": 1
    }
    while True:
        broadcast("request", order)
        print("sent", json.dumps(order))
        sleep(1)

