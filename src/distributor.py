from elevator import Elevator
import network
from watchdog import Watchdog

import threading
import queue
import time
import socket
import sys

# Set elevator id by running the the script with id as the first and only argument. Default id is 1.
MY_ID = 0
if len(sys.argv) - 1 > 0:
    MY_ID = sys.argv[1]
print(f'Elevator running with id {MY_ID}.')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
MY_IP = s.getsockname()[0]
s.close()

# Time to wait for cost from other elevators. In seconds.
ORDER_WATCHER_LIMIT = 0.2

todo = queue.Queue(maxsize=0)
ordersNotAcknowledged = []
ordersAndCosts = []
emptyMessage = {'sender_ip': MY_IP, 'sender_id': MY_ID}

def add_task(task):
    if task not in todo.queue:
        todo.put(task)

def add_task_from_message(data):
    task = data
    if data['type'] == 'cost_request':
        task['type'] = 'get_cost'
    elif data['type'] == 'order':
        task['type'] = 'add_order_or_watchdog'
    elif data['type'] == 'clear_order':
        task['type'] = 'clear_order'
    elif data['type'] == 'cost':
        task['type'] = 'receive_cost'
    elif data['type'] == 'acknowledge_order':
        task['type'] = 'acknowledge_order'
    add_task(task)


#elevator.run(MY_ID, add_task)
elevator = Elevator(MY_ID, add_task)
elevator.run()
#watchdog.run(add_task)
watchdog = Watchdog(add_task)
watchdog.run()
network.run(add_task_from_message)

def order_watcher():
    global ordersAndCosts
    while True:
        current_time = int(time.time())
        popList = []
        for element in ordersAndCosts:
            if element['timestamp'] + ORDER_WATCHER_LIMIT < current_time:
                #print(f'Costs: {element}')
                if len(element['costs']) > 0:
                    lowest_cost = 1000
                    for costElement in element['costs']:
                        if costElement['cost'] < lowest_cost:
                            lowest_cost = costElement['cost']
                            lowest_cost_elevator_id = costElement['sender_id']
                    add_task({'type': 'broadcast_order',
                                        'floor': element['order']['floor'],
                                        'button': element['order']['button'],
                                        'order_elevator_id': lowest_cost_elevator_id
                                        })
                    popList.append(element)
        ordersAndCosts = [element for element in ordersAndCosts if element not in popList]
        time.sleep(ORDER_WATCHER_LIMIT/2)


order_watcher_thread = threading.Thread(target=order_watcher)
order_watcher_thread.start()

while True:
    task = todo.get(True)
    #print(f'Task: {task}')

    if 'sender_ip'          in task: sender_ip = task['sender_ip']
    if 'sender_id'          in task: sender_id = task['sender_id']
    if 'order_elevator_id'  in task: order_elevator_id = task['order_elevator_id']
    if 'floor'              in task: floor = task['floor']
    if 'button'             in task: button = task['button']

    if task['type'] == 'broadcast_cost_request':
        # Insert new element into cost list
        ordersAndCosts[:] = [element for element in ordersAndCosts if not (element['order']['floor'] == floor and element['order']['button'] == button)]
        timestamp = int(time.time())
        element = {'order': {'floor': floor, 'button': button}, 'timestamp': timestamp, 'costs': []}
        ordersAndCosts.append(element)

        message = emptyMessage.copy()
        message['type']   = 'cost_request'
        message['floor']  = floor
        message['button'] = button
        network.broadcast(message)

    elif task['type'] == 'broadcast_order':
        if order_elevator_id == 'MY_ID': order_elevator_id = MY_ID
        message = emptyMessage.copy()
        message['type']              = 'order'
        message['floor']             = floor
        message['button']            = button
        message['order_elevator_id'] = order_elevator_id
        network.broadcast(message)

    elif task['type'] == 'receive_cost':
        cost = task['cost']
        for element in ordersAndCosts:
            if element['order']['floor'] == floor and element['order']['button'] == button:
                element['costs'].append({'sender_id': sender_id, 'cost': cost})
                break

    elif task['type'] == 'broadcast_finished_order':
        message = emptyMessage.copy()
        message['type']              = 'clear_order'
        message['floor']             = floor
        message['order_elevator_id'] = MY_ID
        network.broadcast(message)

    elif task['type'] == 'get_cost':
        cost = elevator.get_cost(floor, button)
        message = emptyMessage.copy()
        message['type']   = 'cost'
        message['floor']  = floor
        message['button'] = button
        message['cost']   = cost
        #network.send(sender_ip, message)
        network.broadcast(message)

    elif task['type'] == 'clear_order':
        watchdog.clear_watchdog(order_elevator_id, floor)
        elevator.clear_lamps(floor)

    elif task['type'] == 'add_order_or_watchdog':
        if MY_ID == order_elevator_id and button == 2:
            elevator.add_order(floor, button)

        if sender_id != MY_ID:
            message = emptyMessage.copy()
            message['type']              = 'acknowledge_order'
            message['order_elevator_id'] = order_elevator_id
            message['floor']             = floor
            message['button']            = button
            #network.send(sender_ip, message)
            network.broadcast(message)
            if button != 2:
                elevator.set_lamp(floor, button)

        if order_elevator_id == MY_ID and sender_id != MY_ID:
            elevator.add_order(floor, button)

        if order_elevator_id != MY_ID:
            watchdog.add_watchdog(order_elevator_id, floor, button)

        if sender_id == MY_ID:
            if order_elevator_id == MY_ID:
                watchdog.add_watchdog(order_elevator_id, floor, button)
            isInList = False
            for order in ordersNotAcknowledged:
                if order == {'order_elevator_id': order_elevator_id, 'floor': floor, 'button': button}:
                    isInList = True
                    break
            if not isInList:
                ordersNotAcknowledged.append({'order_elevator_id': order_elevator_id, 'floor': floor, 'button': button})

    elif task['type'] == 'acknowledge_order': # receive ack
        isInList = False
        i = 0
        for order in ordersNotAcknowledged:
            if order == {'order_elevator_id': order_elevator_id, 'floor': floor, 'button': button}:
                if order_elevator_id == MY_ID:
                    elevator.add_order(floor, button)
                elif button != 2:
                    elevator.set_lamp(floor, button)
                isInList = True
                break
            i = i + 1
        if isInList:
            ordersNotAcknowledged.pop(i)
