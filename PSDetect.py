import sys
import argparse
import socket
import time
from scapy.all import sniff
import signal


# to remember which clients scanned what
pkt_record = {}

global f



def signal_handler(sig, frame):
    f.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



def listen_loop():
    global f
    f = open("detector.txt", "w")
    while(1):
        packets = sniff(iface="lo", prn=process_pkt, store=0)
    f.close()



def process_pkt(pkt):
    global f
    ip_src = str(pkt[1].src)
    port_dst = pkt[2].dport
    #print(port_dst)

    if ip_src not in pkt_record:
        pkt_record[ip_src] = [(port_dst, time.time())]
    elif pkt_record[ip_src] == None:
            ### entry is None if it's already been recorded as
            ### a port scanner
            return
    else:
        purge_old(ip_src)
        #print(pkt_record[ip_src])
        #print(pkt_record[ip_src][-1][0])
        #print(port_dst)

        if pkt_record[ip_src][-1][0] != (port_dst - 1):
            pkt_record[ip_src] = [(port_dst, time.time())]
        elif len(pkt_record[ip_src]) >= 15:
            f.write("Scanner detected. The scanner originated from host " + str(ip_src) + ".\n")
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
 
