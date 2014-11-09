#!/usr/bin/env python3
import ipaddr
import re
import time


def get_ns_db(db="db.shack", ip_db=dict()):
    with open(db, 'r') as dns:
        for line in dns:
            regex = re.compile(";.*?\n")
            line = re.sub(regex, "", line)  # remove comments
            line = line.split()
            if len(line) < 4:
                continue
            if line[1] != "IN" or line[2] != 'A':
                continue
            address = ipaddr.IPAddress(line[3])
            name = line[0]
            ip_db[address] = name
        # for address in network:
        #     name = str(address).replace('.', '-')
        #     ip_db[address] = name
    return ip_db


def revers_dns(net, ns_db=dict()):
    network = ipaddr.IPNetwork(net, strict=False)
    network_address = str(network.network)
    filename = network_address.split('.')[:-1]
    filename.reverse()
    filename = '.'.join(filename) + ".in-addr.arpa"
    zone = filename + "." + " " * max(0, 30 - len(filename))
    serial = time.strftime("%Y%m%d%H%M")
    header = """$TTL    86400
%s IN      SOA     dns.shack. rz.lists.shackspace.de. (
                                %s; Serial
                                604800; Refresh
                                86400; Retry
                                2419200; Expire
                                604800 ); Negative Cache TTL
;
                                IN      NS      dns.shack.
                                IN      NS      fallbackns.shack.

""" % (zone, serial)
    with open("/etc/bind/pri/" + filename, 'w') as output:
        output.write(header)
        for address in network:
            if address in ns_db:
                name = ns_db[address]
            else:
                name = str(address).replace('.', '-')
            suffix = str(address).split('.')[-1]
            suffix = suffix + " " * max(0, 31 - len(suffix))
            output.write("%s IN      PTR     %s.shack.\n" % (suffix, name))


def main():
    ns_db = get_ns_db("/etc/bind/pri/db.shack")
    for i in range(256):
        revers_dns("10.42.%i.0/24" % i, ns_db)


if __name__ == "__main__":
    main()
