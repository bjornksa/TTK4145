import subprocess
import socket
import time
import multiprocessing
import threading
from threading import Timer
import os
import argparse


class Counter:
    def __init__(self, current_number = 0, master = False):
        self.current_number = current_number
        self.is_master = master
        self.socket = None
        self.IP = "127.0.0.1"
        self.PORT = 5005

        if self.is_master:
            self.spawn_backup()
            self.master_loop()

        else:
            self.backup_loop()

    def master_loop(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            for i in range(10):
                time.sleep(0.1)
                self.broadcast_status()
            self._increment()
            self.print_curr_num()

    def backup_loop(self):
        msg_timer = Timer(1.0, self.become_master)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.socket.bind((self.IP, self.PORT))

        msg_timer.start()

        print("This is backup speaking")

        while True:
            if (self.socket.recv != None):
                data = int.from_bytes(self.socket.recv(10), byteorder='big')
                print("bu:",data)
                self.current_number  = data

                msg_timer.cancel()
                msg_timer.join()

                msg_timer = Timer(1.0, self.become_master)
                msg_timer.start()

            if (not msg_timer.is_alive()):
                msg_timer.join()
                break


    def spawn_backup(self):
        script_path = os.path.join(__file__)
        backup = subprocess.Popen("gnome-terminal -- python3 " + script_path + " -b True", shell=True)

    def become_master(self):
        #self.socket.shutdown(socket.SOCK_DGRAM)
        self.socket.close()
        self.spawn_backup()
        self.is_master = True
        self.master_loop()

    def broadcast_status(self):
        self.socket.sendto(bytes([self.current_number]), (self.IP, self.PORT))

    def print_curr_num(self):
        print(self.current_number)
        # threads = threading.enumerate()
        # print(threads)

    def _increment(self):
        self.current_number += 1



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-b", "--backup", type=bool, help="Spawn as backup")
    args = parser.parse_args()

    if args.backup:
        counter = Counter()
    else:
        master = Counter(master=True)


if __name__ == "__main__":
    main()

