import elevator
import network
import watchdog

import threading
import queue
import time
import socket
import sys

# Set elevator id by running the the script with id as the first and only argument
elevator_id = 1
if len(sys.argv) - 1 > 0:
    elevator_id = sys.argv[1]
print(f'Elevator running with id {elevator_id}.')

ORDER_WATCHER_LIMIT = 0.5
MY_IP = socket.gethostname()

todo = queue.Queue(maxsize=0)

def add_to_distributor(task):
    todo.put(task)

ordersNotAcknowledged = []
ordersAndCosts = []

elevator.run(add_to_distributor)
watchdog.run(add_to_distributor)
network.run(add_to_distributor)

def order_watcher():
    while True:
        flag = False
        current_time = int(time.time())
        j = 0
        for element in ordersAndCosts:
            timestamp = element[1]
            if timestamp + ORDER_WATCHER_LIMIT < current_time:
                if element[2]:
                    lowest_cost_ip = element[2][0]
                    lowest_cost = element[2][1]
                    for i in range(3, len(element)):
                        if element[i][1] < lowest_cost:
                            lowest_cost = element[i][1]
                            lowest_cost_ip = element[i][0]
                    network.broadcast('order', {'floor': floor, 'button': button, 'order_ip': lowest_cost_ip})
                    flag = True
                    break #ehhh dette må fikses
            j = j + 1
        if j > 0 and j < len(ordersAndCosts):
            ordersAndCosts.pop(j)

        if flag:
            ordersAndCosts.pop()
        time.sleep(0.1)

order_watcher_thread = threading.Thread(target=order_watcher)
order_watcher_thread.start()

while True:
    do = todo.get(True)
    print(f'ddo: {do}')

    if 'sender_ip' in do: sender_ip = do['sender_ip']
    if 'order_ip' in do:  order_ip = do['order_ip']
    if 'floor' in do:     floor = do['floor']
    if 'button' in do:    button = do['button']

    if do['type'] == 'broadcast_order':
        network.broadcast('cost_request', {'floor': floor, 'button': button})

    elif do['type'] == 'receive_cost':
        alreadyInList = False
        for element in ordersAndCosts:
            if element[0] == {floor, button}:
                costElement = []
                costElement.append(sender_ip)
                costElement.append(cost)
                element.append(costElement)
                alreadyInList = True
                break
        if not alreadyInList:
            timestamp = int(time.time())
            element = []
            element.append({floor, button})
            element.append(timestamp)
            costElement = []
            costElement.append(sender_ip)
            costElement.append(cost)
            element.append(costElement)
            ordersAndCosts.append(element)

    elif do['type'] == 'broadcast_finished_order':
        order_ip = MY_IP
        network.broadcast('clear_order', {'floor': floor, 'ip': order_ip})

    elif do['type'] == 'get_cost':
        cost = elevator.get_cost(floor, button)
        network.send(sender_ip, 'cost', {'cost': cost, 'floor': floor, 'button': button})

    elif do['type'] == 'clear_order':
        watchdog.clear_watchdog(order_ip, floor)
        elevator.clear_lamps(floor)

    elif do['type'] == 'add_order_or_watchdog':
        if MY_IP == order_ip:
            elevator.add_order(floor, button)
        else:
            watchdog.add_watchdog(order_ip, floor, button)

        if MY_IP == sender_ip:
            alreadyInList = False
            for order in ordersNotAcknowledged:
                if order == {order_ip, floor, button}:
                    alreadyInList = True
                    break
            if not alreadyInList:
                ordersNotAcknowledged.append({order_ip, floor, button})
        else:
            network.send('acknowledge_order', {'floor': floor, 'button': button}) #her er det feil
            elevator.set_lamp(floor, button)

    elif do['type'] == 'acknowledge_order':
            isInList = False
            i = 0
            for order in ordersNotAcknowledged:
                if order == {order_ip, floor, button}:
                    isInList = True
                    break
                i = i + 1
            if isInList:
                elevator.set_lamp(floor, button)
                ordersNotAcknowledged.pop(i)
