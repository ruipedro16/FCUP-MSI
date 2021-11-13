#!/usr/bin/env python3

import sys
import time
from scapy.all import *


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.stderr.write(f'Invalid number of arguments\n \
                           Usage: ./parser <file path>')
        sys.exit(1)

    start_time = time.time()

    try:
        ip_addr = [(p[IP].src, p[IP].dst)
                   for p in rdpcap(sys.argv[1]) if IP in p]
        src_addr = set(x[0] for x in ip_addr)
        dst_addr = set(x[1] for x in ip_addr)
    except FileNotFoundError:
        sys.stderr.write(f'File {sys.argv[1]} not found\n')
        sys.exit(1)

    print('SRC IP ADDR')
    for addr in src_addr:
        print(addr)

    print('\n\nDST IP ADDR')
    for addr in dst_addr:
        print(addr)

    elapsed_time = time.time() - start_time

    print(f'\nElapsed time: {elapsed_time} seconds')
