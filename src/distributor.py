import elevator
import network
import watchdog

import threading
import queue
import time
import socket
import sys

# Set elevator id by running the the script with id as the first and only argument. Default id is 1.
MY_ID = 1
if len(sys.argv) - 1 > 0:
    MY_ID = sys.argv[1]
print(f'Elevator running with id {MY_ID}.')

MY_IP = socket.gethostname()
ORDER_WATCHER_LIMIT = 0.5
todo = queue.Queue(maxsize=0)
ordersNotAcknowledged = []
ordersAndCosts = []
emptyMessage = {'sender_ip': MY_IP, 'sender_id': MY_ID}

def add_to_distributor(task):
    todo.put(task)

elevator.run(add_to_distributor)
watchdog.run(add_to_distributor)
network.run(add_to_distributor)

def order_watcher():
    global ordersAndCosts
    while True:
        current_time = int(time.time())
        popList = []
        for element in ordersAndCosts:
            if element['timestamp'] + ORDER_WATCHER_LIMIT < current_time:
                if len(element['costs']) > 0:
                    lowest_cost = 0
                    for costElement in element['costs']:
                        lowest_cost = costElement['cost']
                        lowest_cost_ip = costElement['sender_ip']
                    message = emptyMessage
                    message['type']     = 'order'
                    message['floor']    = element['order']['floor']
                    message['button']   = element['order']['button']
                    message['order_ip'] = lowest_cost_ip
                    network.broadcast(message)
                    popList.append(element)
        ordersAndCosts = [element for element in ordersAndCosts if element not in popList]
        time.sleep(0.1)


order_watcher_thread = threading.Thread(target=order_watcher)
order_watcher_thread.start()

while True:
    do = todo.get(True)
    print(f'Do: {do}')

    if 'sender_ip' in do: sender_ip = do['sender_ip']
    if 'order_ip'  in do: order_ip = do['order_ip']
    if 'floor'     in do: floor = do['floor']
    if 'button'    in do: button = do['button']

    if do['type'] == 'broadcast_order':
        message = emptyMessage
        message['type']   = 'cost_request'
        message['floor']  = floor
        message['button'] = button
        network.broadcast(message)

    elif do['type'] == 'receive_cost':
        isInList = False
        for element in ordersAndCosts:
            if element['order']['floor'] == floor and element['order']['button'] == button:
                element['costs'].append({'sender_ip': sender_ip, 'cost': cost})
                isInList = True
                break
        if not isInList:
            timestamp = int(time.time())
            element = {'order': {'floor': floor, 'button': button}, 'timestamp': timestamp, 'costs': [{'sender_ip': sender_ip, 'cost': cost}]}
            ordersAndCosts.append(element)

    elif do['type'] == 'broadcast_finished_order':
        order_ip = MY_IP
        message = emptyMessage
        message['type']     = 'clear_order'
        message['floor']    = floor
        message['order_ip'] = order_ip
        network.broadcast(message)

    elif do['type'] == 'get_cost':
        cost = elevator.get_cost(floor, button)
        message = emptyMessage
        message['type']   = 'cost'
        message['floor']  = floor
        message['button'] = button
        message['cost']   = cost
        network.send(sender_ip, message)

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
            message = emptyMessage
            message['type']   = 'acknowledge_order'
            message['floor']  = floor
            message['button'] = button
            network.send(sender_ip, message)
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
