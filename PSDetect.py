import sys
import argparse
import socket
import time
from scapy.all import sniff
import signal


# to remember which clients scanned what
pkt_record = {}



def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



def listen_loop():
    while(1):
        packets = sniff(iface="lo", prn=process_pkt, store=0)



def process_pkt(pkt):
    ip_src = str(pkt[1].src)
    port_dst = pkt[2].dport

    if ip_src not in pkt_record:
        pkt_record[ip_src] = [(port_dst, time.time())]
    elif pkt_record[ip_src] == None:
            ### entry is None if it's already been recorded as
            ### a port scanner
            return
    else:
        purge_old(ip_src)

        if len(pkt_record[ip_src]) >= 14:
            print("Scanner detected. The scanner originated from host " + str(ip_src) + ".")
            pkt_record[ip_src] = None 
        else:
            pkt_record[ip_src].append((port_dst, time.time()))



def purge_old(str_ip):
    purge_time = time.time()
    for i in range(len(pkt_record[str_ip])):
        (port, t) = pkt_record[str_ip][i]
        if (purge_time - t) > 300:
            pkt_record[str_ip].pop(i)
        


def main():
    listen_loop()


if __name__ == "__main__":
    main()
 
