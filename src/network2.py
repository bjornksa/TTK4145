"""Network protocoll to use tcp to make up for packet loss in elevator alg
"""
import threading
import socket
import threading
from time import sleep
import pprint
import json

class Network_manager():

    broadcast_port = 1440 # kanskje dumt å bare iterere en slik opp
 
    def __init__(self, callback, id):
        self.connections = {}
        self.id = id

    def _broadcast_adress(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        id_dict = {'elev_id': self.id}
        id_str = json.dumps(id_dict)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        while True:
            s.sendto(id_str.encode(), ("255.255.255.255", Network_manager.broadcast_port))
            sleep(1.0)

    def _listen_for_adress(self):
        receiv_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiv_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        receiv_s.bind(("", Network_manager.broadcast_port))
        while True:
            data, addr = receiv_s.recvfrom(1024)
            self._hande_incomming_adress(data, addr)


    def _hande_incomming_adress(self, data, addres):
        print(f'manager {self.id} received data: {data} addres: {addres}')

    """
    def send():
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005
        BUFFER_SIZE = 1024
        MESSAGE = b"Hello, World!"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        s.close()

        print(f"received data: {data}")


    def receive():
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005
        BUFFER_SIZE = 20  # Normally 1024, but we want fast response

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

        conn, addr = s.accept()
        print(f"Connection address: {addr}")
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            print(type(conn))
            print(f"received data: {data}")
            conn.send(data)  # echo
        conn.close()
    """

    def run(self):
       broadcast_thread = threading.Thread(target=self._broadcast_adress)
       listen_thread = threading.Thread(target = self._listen_for_adress)

       broadcast_thread.start()
       listen_thread.start()


if __name__ == "__main__":
    m1 = Network_manager(lambda x: pprint.pprint(x) , 1)
    m2 = Network_manager(lambda x: pprint.pprint(x) , 2)

    m1.run()
    m2.run()

