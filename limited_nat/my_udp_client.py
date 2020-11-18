# -*- coding:utf-8 -*-
"""
author: zhou zhen
date:   2020/11/13

"""
from socket import *
from port_setting import ADDR, BUFFSIZE
import re
from threading import Thread
from time import sleep
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
            if data_out.startswith('{send_to'):
                host_addr = re.findall('^{send_to:(.*)}$', data_out)[0]
                #host_addr = (host_addr.split(',')[0][2:-1], int(host_addr.split(',')[1][:-1]))
                host_addr=eval(host_addr)
                udp_cli_socket.sendto(b'hello', host_addr)
            elif data_out.startswith('{'):
                peer_addrs = eval(data_out)
            else:
                pass

def input_to():
    global peer_addrs
    while True:
        data_in = input()
        if data_in:
            if data_in.startswith('{'):
                if data_in.startswith('{register'):
                    udp_cli_socket.sendto(data_in.encode('utf-8'), ADDR)
                if data_in.startswith('{to_peer'):
                    host = re.findall('^{to_peer:(.*)}$', data_in)[0]
                    if host in peer_addrs.keys():
                        peer_addr = peer_addrs[host]
                        #data_in='{to_peer:'+str(peer_addr)+'}'
                        udp_cli_socket.sendto(data_in.encode('utf-8'), ADDR)
                        sleep(1)
                        udp_cli_socket.sendto(b'hello', peer_addr)
                    else:
                        print('no host address!')
            else:
                udp_cli_socket.sendto(data_in.encode('utf-8'), ADDR)

def main():
    t2 = Thread(target=output_in, args=())
    t2.start()
    t1 = Thread(target=input_to, args=())
    t1.start()

if __name__ == '__main__':
    main()