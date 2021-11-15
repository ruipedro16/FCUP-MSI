#!/bin/sh

echo "{SSHA512}FhFw5Pfw6kQEiSP4+tSkew5kdRzCdtqGaybFFRsPH1OA1oUYqkLdDSg6WzfRCoL3FN1pXyGq9OlE+1iYCUI0uFsG9FNFwls3" >hash.txt
hashcat -a 3 -m 1711 hash.txt -1 ?l?d ?1?1?1?1?1?1?1?1?1?1 --increment --increment-min 4 --increment-max 10 >/dev/null 2>&1
PASSWORD=$(hashcat -m 1711 hash.txt -- show | cut -d : -f 1)
echo "TPAS{$PASSWORD}"
rm hash.txt
