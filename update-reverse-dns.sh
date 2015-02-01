#!/bin/sh

/root/reversedns/gen_reverse_dns.py

for i in $(seq 0 255) 
do
	rndc reload ${i}.42.10.in-addr.arpa > /dev/null
done

for net in 0.0.10 1.0.10
do
	rndc reload ${net}.in-addr.arpa > /dev/null
done
