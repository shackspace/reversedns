#!/usr/bin/env python3
try:
    import ipaddress
except ImportError:
    import ipaddr as ipaddress
import re


HEADER = """$TTL    86400
0.42.10.in-addr.arpa.           IN      SOA     dns.shack. rz.lists.shackspace.de. (
                                2014072502; Serial
                                604800; Refresh
                                86400; Retry
                                2419200; Expire
                                604800 ); Negative Cache TTL
;
                                IN      NS      dns.shack.
                                IN      NS      fallbackns.shack.

"""


def get_ns_db():
    ip_db = dict()
    with open("db.shack", 'r') as dns:
        for line in dns:
            regex = re.compile(";.*?\n")
            line = re.sub(regex, "", line)  # remove comments
            line = line.split()
            if len(line) < 4:
                continue
            if line[1] != "IN" or line[2] != 'A':
                continue
            address = ipaddress.ip_address(line[3])
            name = line[0]
            ip_db[address] = name
        # for address in network:
        #     name = str(address).replace('.', '-')
        #     ip_db[address] = name
    return ip_db


def revers_dns(net, ns_db=dict()):
    network = ipaddress.ip_network(net, strict=False)
    network_address = str(network.network_address)
    filename = network_address.split('.')[:-1]
    filename.reverse()
    filename = '.'.join(filename) + ".in-addr.arpa"
    with open(filename, 'w') as output:
        output.write(HEADER)
        for address in network:
            if address in ns_db:
                name = ns_db[address]
            else:
                name = str(address).replace('.', '-')
            suffix = str(address).split('.')[-1]
            output.write("%31s IN      PTR     %s.shack.\n" % (suffix, name))


def main():
    ns_db = get_ns_db()
    for i in range(256):
        print(i)
        revers_dns("10.42.%i.0/24" % i, ns_db)


if __name__ == "__main__":
    main()
