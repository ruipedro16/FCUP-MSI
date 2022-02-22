#!/bin/sh

BASEDIR=$(pwd)
dirsearch -u "http://tpas.alunos.dcc.fc.up.pt:5015/" -o "$BASEDIR/tmp.txt" >/dev/null 2>&1
URL=$(grep "well-known" "$BASEDIR/tmp.txt" | cut -d " " -f 7)
curl --silent "$URL" | grep -oE "TPAS{.+}" --color=none
rm "$BASEDIR/tmp.txt"
