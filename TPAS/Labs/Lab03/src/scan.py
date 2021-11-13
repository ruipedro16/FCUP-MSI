#!/usr/bin/env python3

import re
import sys
import time
from scapy.all import *


"""
This script must be run with root privileges

$ sudo ./scan.py <IP address of host> <Port Range>

E.g.

$ sudo ./scan.py 193.136.39.125 1-1024

Scans ports sequentially
Could be improved by taking advantage of multithreading
"""


def is_up(host_addr, timeout=1):
    """
    pings a host to check if it is up
    """
    packet = IP(dst=host_addr)/ICMP()
    resp = sr1(packet, timeout=timeout, verbose=False)
    return resp is not None


def is_open(host_addr, port):
    """
    checks if a port is open
    """
    src_port = RandShort()
    packet = IP(dst=host_addr) / TCP(sport=src_port, dport=port, flags='S')
    resp = sr1(packet, timeout=2)

    if resp is None:
        return False
    elif resp.haslayer(TCP):
        if resp.getlayer(TCP).flags == 0x12:  # SYN/ACK
            rst = sr(IP(dst=host_addr) / TCP(sport=src_port,
                                             dport=port, flags='AR'), timeout=2)
            return True
    elif resp.getlayer(TCP) == 0x14:  # RST/ACK
        return False


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write(f'Invalid number of arguments\n \
                           Usage: sudo ./scan.py <IP address of host> <Port Range>')
        sys.exit(1)

    target_addr = sys.argv[1]

    if not re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', target_addr):
        sys.stderr.write('Invalid IPv4 address\n')
        sys.exit(1)

    try:
        [min_port, max_port] = map(int, sys.argv[2].split('-'))
    except ValueError:
        sys.stderr.write('Invalid port range\n')
        sys.exit(1)

    conf.verb = 0  # Disable verbose in sr() and sr1()

    start_time = time.time()

    if is_up(target_addr):
        print(f'Scanning host {target_addr}')
        open_ports = list(filter(lambda p: is_open(
            target_addr, p), range(min_port, max_port + 1)))
        elapsed_time = time.time() - start_time
        print(f'Scan completed \t Elapsed time: {elapsed_time} seconds')
        print(f'Open Ports: {open_ports}')
    else:
        sys.stderr.write(f'Host {target_addr} is not up\n')
        sys.exit(1)
