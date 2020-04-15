"""Launch n connected elevator simulators and distributors
"""
import argparse
import os
import sys

base_sim_socet = 15657
base_dir = os.path.dirname(os.path.abspath(__file__))
print(base_dir)



parser = argparse.ArgumentParser(description='script to run elevator servers and elevator distributors')
parser.add_argument('num_elev', type=int, help='the number of elevator and elevatorservers to start')
args = parser.parse_args()
num_elev = args.num_elev

print(f'launching {num_elev} servers and distributors')
for i in range(num_elev):
    print(f'launched: {i}')
    os.system(f'gnome-terminal -e \'sh -c \"cd {base_dir}; ./SimElevatorServer --port {base_sim_socet+i}; exec bash\"\'') # run simulator in new terminal
    os.system(f'gnome-terminal -e \'sh -c \"cd {os.path.join(base_dir,"src")}; python3 distributor.py {0}; exec bash\"\'') # run distributor in new terminal