import subprocess
import socket
import time
import multiprocessing
import threading
from threading import Timer
import os
import argparse


class Counter:

    _current_number = None
    _is_master = None
    _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP = "127.0.0.1"
    PORT = 5005


    def __init__(self, current_number = 0, master = False):
        self.current_number = current_number
        self.is_master = master

        if self.is_master:
            self.spawn_backup()
            self.master_loop()

        else:
            self.backup_loop()

    def master_loop(self):
        while True:
            for i in range(10):
                time.sleep(0.1)
                self.broadcast_status()
            self._increment()
            self.print_curr_num()

    def backup_loop(self):
        msg_timer = Timer(1.0, self.become_master)
        self._socket.bind((self.IP, self.PORT))
        msg_timer.start()

        while True:
            if (self._socket.recv != None):
                self.current_number = self._socket.recv(10)
                msg_timer.cancel()
                msg_timer.start()

            if (not msg_timer.is_alive()):
                msg_timer.join()
                break


    def spawn_backup(self):
        script_path = os.path.join(os.path.dirname(__file__), "ex_6.py -b True")
        backup = subprocess.Popen("python3 " + script_path)
    def become_master(self):
        self.spawn_backup()
        self.master_loop()

    def broadcast_status(self):
        self._socket.sendto(bytes(self.current_number), (self.IP, self.PORT))

    def print_curr_num(self):
        print(self.current_number)
        threads = threading.enumerate()
        print(threads)

    def _increment(self):
        self.current_number += 1



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-b", "--backup", type=bool, help="Spawn as backup")
    args = parser.parse_args()

    if args.backup:
        counter = Counter
    else:
        master = Counter(master=True)


if __name__ == "__main__":
    main()

