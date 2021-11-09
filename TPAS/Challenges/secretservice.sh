#!/bin/sh

nmap -sV -p 5000-7000 tpas.alunos.dcc.fc.up.pt -oN tmp.txt >/dev/null 2>&1

# 5015, the first port running http, hosts the website for the "Bug Bounty" challenge
PORT=$(grep -E "open[[:space:]]+http" tmp.txt | tail -n 1 | cut -d '/' -f 1)
curl --insecure --silent "tpas.alunos.dcc.fc.up.pt:$PORT" | grep -oE "TPAS{.+}" 
rm tmp.txt
