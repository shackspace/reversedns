#!/bin/sh

/root/reversedns/gen_reverse_dns.py

for i in $(seq 0 255) 
do
	rndc reload ${i}.42.10.in-addr.arpa > /dev/null
done
