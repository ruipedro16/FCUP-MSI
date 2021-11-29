#!/usr/bin/env python3

import angr
import claripy

success_addr = 0x004006dc
failure_addr = 0x0040078e
base_addr = 0x00400000

flag_len = 36

p = angr.Project('./myfirstelf', main_opts={
    "base_addr": base_addr
})

flag_chars = [claripy.BVS(f'flag_char{i}', 8) for i in range(flag_len)]
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')])

state = p.factory.full_init_state(
    args=['./myfirstelf'],
    add_options=angr.options.unicorn,
    stdin=flag,
)

# Add constraints that all characters are printable
for k in flag_chars:
    state.solver.add(k >= ord('!'))
    state.solver.add(k <= ord('~'))

simgr = p.factory.simulation_manager(state)
simgr.explore(find=success_addr, avoid=failure_addr)

if (len(simgr.found) > 0):
    for found in simgr.found:
        print(found.posix.dumps(0)[:-1])
