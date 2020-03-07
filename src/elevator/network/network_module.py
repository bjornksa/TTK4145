import json
import socket
from multiprocessing import Process, Queue
from pprint import pformat
from time import sleep

def receiv(q):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 12345))
    while True:
        data = server_socket.recvfrom(1024)
        json_data = json.loads(data[0].decode())
        #print('reveiver receiver: \n' + pformat(json_data) + '\n')
        q.put(json_data)


def send(q):
    sending_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        json_data = q.get()
        print('sender sent: \n' + pformat(json_data) + '\n')
        data = json.dumps(json_data)
        sending_socket.sendto(data.encode(), ('localhost', 12345))


def make_network_manager(send_queue):
    """ Makes two processes that sends and receives data packages with UDP.
    
    Arguments:
        send_queue {multiprocessing.Queue} -- a Queue where packages to be sendt are put
    
    Returns:
        [multiprocesing.Queue] -- A Queue where received packages are put
    """
    receive_queue = Queue()
    receive_p = Process(target=receiv, args=(receive_queue,))
    send_p = Process(target=send, args=(send_queue,))
    receive_p.daemon = True
    send_p.daemon = True
    receive_p.start()
    send_p.start()
    return receive_queue


def que_printer(q):
    while True:
        data = q.get()
        print(data)

def network_manager_tester():
    send_queue = Queue()
    receiv_queue = make_network_manager(send_queue)
    counter = 0

    que_reader = Process(target=que_printer, args=(receiv_queue,))
    que_reader.daemon = True
    que_reader.start()

    while True:
        sleep(1.0)
        order = {
            "count": counter,
            "elevator": 1,
            "elevator_ip": "192.168",
            "order_floor": 2,
            "order_type":"internal",
            "order_dir": 1
        }
        send_queue.put(order)
        counter += 1


if __name__ == "__main__":
    network_manager_tester()
