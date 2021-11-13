# Lab 03 - Network Scanning

## 1

Target: open.tinder.com

Using `netcat`, we know that the server running is openresty/1.19.3.1

```
echo " " | nc open.tinder.com 80

HTTP/1.1 400 Bad Request
Server: openresty/1.19.3.1
Date: Tue, 09 Nov 2021 23:36:28 GMT
Content-Type: text/html
Content-Length: 163
Connection: close
X-Proxy-Me: afcdpt_cdproxy-29003-001-prod.eu1.appsflyer.com

<html>
<head><title>400 Bad Request</title></head>
<body>
<center><h1>400 Bad Request</h1></center>
<hr><center>openresty/1.19.3.1</center>
</body>
</html>

```

This can also be achieved by with the `curl`command

```
curl -s -I open.tinder.com

HTTP/1.1 403 Forbidden
Server: openresty/1.19.3.1
Date: Tue, 09 Nov 2021 23:37:18 GMT
Content-Type: text/html
Content-Length: 159
Connection: keep-alive
X-Proxy-Me: afcdpt_cdproxy-29003-001-prod.eu1.appsflyer.com
```

## 2

### 2.1

We can perform a ping scan and output the result to file `2.1.txt` by running `nmap -sn -v tpas.alunos.dcc.fc.up.pt -oN 2.1.txt`

### 2.2

We can perform an aggressive scan with the `-A` flag. For example, we can perform an aggressive scan and output the result to file `2.2.txt` by running `nmap -A -v -oN 2.2.txt tpas.alunos.dcc.fc.up.pt`

### 2.3

We can scan for a port range with the `-p` flag. For example, we can scans the ports ranging from 1 to 1000 and output the result to file `2.3.txt` by running `nmap -p 1-1000 -v -oN 2.3.txt tpas.alunos.dcc.fc.up.pt`

### 2.4

We can perform a listen scan with the `-sL` flag. For example, we can perform a listen scan on a home network and output the result to file `2.4.txt` by running `nmap -sL -v -oN 2.4.txt 192.168.1.0/24`

## 3

The ping scan leads to less network traffic when compared to the other types of scan:

-   Aggressive Scan: 3661 packets
-   Listen Scan: 512 packets
-   Ping Scan: 13 packets
-   Port Scan: 2018 packets

## 4

TPAS{y0u_just_f0und_a_s3cr3t_s3rv1ce}

## 5

## 5.1

By running `nmap -sV tpas.alunos.dcc.fc.up.pt -oX /dev/stdout`, we can know what services are running and their respective version.
The CPEs can also be listed by running `nmap -sV tpas.alunos.dcc.fc.up.pt -oX /dev/stdout | grep -oE "<cpe>.*</cpe>" | uniq`:

```
<cpe>cpe:/a:apache:http_server:2.4.29</cpe>
```

This way, we know that there's an Apache HTTP server running and its version is 2.4.29

Searching for this specific version, the following CVEs were found:

-   CVE-2021-40438
-   CVE-2021-39275
-   CVE-2021-34798
-   CVE-2021-33193
-   CVE-2021-32792
-   CVE-2021-32791
-   CVE-2021-32786
-   CVE-2021-32785
-   CVE-2021-26691
-   CVE-2021-26690
-   CVE-2020-35452
-   CVE-2020-13938
-   CVE-2019-17567
-   CVE-2020-9490
-   CVE-2020-11993
-   CVE-2020-1927
-   CVE-2020-1934
-   CVE-2019-10092
-   CVE-2019-10082
-   CVE-2019-10098
-   CVE-2019-10081
-   CVE-2019-0197
-   CVE-2019-0196
-   CVE-2019-0220
-   CVE-2019-0211
-   CVE-2019-0217
-   CVE-2018-17199
-   CVE-2018-17189
-   CVE-2018-11763
-   CVE-2018-1333
-   CVE-2018-1312
-   CVE-2018-1303
-   CVE-2018-1302
-   CVE-2018-1301
-   CVE-2018-1283
-   CVE-2017-15715
-   CVE-2017-15710

## 5.2

[Source Code](src/parser.py)

```py
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
```

For example, running `./parser.py ../results/wireshark/port-scan.pcapng` outputs the following:

```
SRC IP ADDR
10.0.2.15
193.136.39.125
192.168.1.1


DST IP ADDR
10.0.2.15
193.136.39.125
192.168.1.1

Elapsed time: 0.37662744522094727 seconds
```

This results can be checked in `Wireshark`: Statistics > IPv4/IPv6 Statistics > Source and Destination Addressess

## 5.3

[Source Code](src/scan.py) => This script must be run with root privileges

```py
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
```

For example, running `sudo ./scan.py 193.136.39.125 1-1024` outputs the following:

```
Scanning host 193.136.39.125
Scan completed   Elapsed time: 86.81599164009094 seconds
Open Ports: [80, 443]
```
