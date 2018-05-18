#!/usr/local/bin/python
from scapy.all import *
ipsec_server = "192.168.84.128"

##### Phase 1 #####

# capturing TWO 1st pk from UE and ePDG
#packet1=sniff(iface="eth0", filter="udp and port 500", count=2, prn=lambda x: x.summary)

packet1=sniff(iface="eth0", filter="udp and port 500", count=2)


# forwarding 1st request pk from ue to swan server
data1 = ""		
tlayer =packet1[0].getlayer(UDP)	
#if packet1[0].getlayer(Raw):	
if packet1[0].getlayer(ISAKMP):	
   data1 += str(tlayer.payload)
wrpcap("data1.pcap", packet1[0])  # overall packet 
f = open("raw_data1.dat", 'w')
f.write(data1)
f.close()

# storing 2nd response pk from ePDG
data2 = ""
tlayer =packet1[1].getlayer(UDP)	
#if packet1[1].getlayer(Raw):	
if packet1[1].getlayer(ISAKMP):	
   data2 += str(tlayer.payload) #assemble the packet

wrpcap("data2.pcap", packet1[1])  # overall packet 
#wireshark(packet1[1])
f = open("raw_data2.dat", 'w')    # payload only
f.write(data2)
f.close()

send(IP(dst=ipsec_server)/UDP()/ISAKMP(data1))





