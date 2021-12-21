#!/bin/sh

zip2john flag.zip >tmp 2>/dev/null
john tmp >/dev/null 2>&1
PASSWORD=$(john --show tmp | cut -d ":" -f 2 | head -n 1)
rm tmp
unzip -P "$PASSWORD" flag.zip >/dev/null
cat flag.txt
rm flag.txt
