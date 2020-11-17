# -*- coding:utf-8 -*-
"""
author: zhou zhen
date:   2020/11/14

"""
from socket import *
from port_setting import ADDR, BUFFSIZE

import re

clients = {}

'''def get_addr(handler, data: str,address:tuple):
    host = re.findall('^{require:(.*)}$', data)
    host = host[0].lstrip()
    result = clients[host]
    if result is None:
        handler.sendto(b'No host address,sorry.',address)
    else:
        handler.sendto(b'address:', result.encode('utf-8'),address)'''


def register(handler, data: str, address: tuple):
    data = re.findall('^{register:(.*)', data)[0]
    if data:
        if address not in clients.values() and data not in clients.keys():
            clients[data] = address
        elif clients[data]:
            handler.sendto(b'this host name already registered', address)
        else:
            for k in clients.keys():
                if clients[k] == address:
                    clients.pop(k)
                    break
            clients[data] = address
        for addr in clients.values():
            handler.sendto(clients.__repr__().encode('utf-8'), addr)  # 广播现有地址
        print(clients)


'''def timer_thread(handler):
    while True:
        for k in clients.keys():
            handler.sendto(b'alive?',clients[k])
            print(clients[k])
            if handler.recvfrom(BUFFSIZE):
                pass
            else:
                clients.pop(k)
                print(clients)'''


def send_across(handler, data: str, address: tuple):
    host = re.findall('^{to_peer:(.*)', data)[0]
    addr = clients[host]
    msg = '{send_to:%s}' % str(address)
    handler.sendto(msg.encode('utf-8'), addr)


def main():
    udp_server = socket(AF_INET, SOCK_DGRAM)
    udp_server.bind(ADDR)
    print('waiting for connection....')
    while True:
        data, addr = udp_server.recvfrom(BUFFSIZE)
        print('connect from %s' % str(addr))
        if data:
            data = data.decode('utf-8')
            data = data[:-1]
            if data.startswith('{register:'):
                register(udp_server, data, addr)
            elif data.startswith('{to'):
                send_across(udp_server, data, addr)
            else:
                udp_server.sendto(b'Do not provide this service', addr)


if __name__ == '__main__':
    main()
