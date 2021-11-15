#!/bin/sh

curl --insecure --silent "https://tpas-desafios.alunos.dcc.fc.up.pt/" | grep -oE "TPAS{.+}" --color=none
