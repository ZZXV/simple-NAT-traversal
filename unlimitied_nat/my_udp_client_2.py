# -*- coding:utf-8 -*-
"""
author: zhou zhen
date:   2020/11/13

"""
from socket import *
from port_setting import ADDR, BUFFSIZE
import re
from threading import Thread

udp_cli_socket = socket(AF_INET, SOCK_DGRAM)
global peer_addrs
peer_addrs = {}


def output_in():
    global peer_addrs
    while True:
        data_out = udp_cli_socket.recvfrom(BUFFSIZE)
        if data_out:
            data_out = data_out[0].decode('utf-8')
            print(data_out)
            if str(data_out).startswith('{'):
                peer_addrs = eval(data_out)


def input_to():
    global peer_addrs
    while True:
        data_in = input()
        if data_in.startswith('{register'):
            udp_cli_socket.sendto(data_in.encode('utf-8'), ADDR)
        if data_in.startswith('{to_peer'):
            host = re.findall('^{to_peer:(.*)}$', data_in)[0]
            if host == 'all':
                for var in peer_addrs.values():
                    udp_cli_socket.sendto(b'hello', var)
            else:
                if host in peer_addrs.keys():
                    peer_addr = peer_addrs[host]
                    udp_cli_socket.sendto(b'hello', peer_addr)
                else:
                    print('no host address!')


def main():
    t2 = Thread(target=output_in, args=())
    t2.start()
    t1 = Thread(target=input_to, args=())
    t1.start()

if __name__ == '__main__':
    main()