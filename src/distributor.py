import elevator
import network
import watchdog

import queue

todo = queue.Queue(maxsize=0)

def add_to_distributor(task):
    todo.put(task)

elevator.run(add_to_distributor)
watchdog.run()
network.run()

while True:
    do = todo.get(True)
    print(f'do: {do}')
    #do something with it
