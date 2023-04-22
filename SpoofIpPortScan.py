from scapy.all import *

ans, uans = sr(IP(dst="localhost", src="192.168.1.1")/TCP(dport=list(range(10000,15000)),flags="A"))


ans, uans = sr(IP(dst="localhost", src="192.164.1.1")/TCP(dport=[(2*i) + 10000 for i in range(2000)],flags="A"))


ans, uans = sr(IP(dst="localhost", src="192.169.11.11")/TCP(dport=list(range(20000,45000)),flags="A"))
