#!/usr/bin/python
import sys
import os
import getopt
from scapy.all import *

def usage():
    print 'For help: "./rogueAp.py -h" or "./rogueAp.py --help"'
    print "Usage: ./rogueAp.py -i <Wired_interface> -o <WiFi_interface> -a <IPSEC_server_addr>"

def packet_proc():
    #TODO: Fix this module later
    # capture first 2 isakmp packets from input (i.e., Rogue-AP interface)
    for pkt in sniff(iface=wired_intf, filter="udp and port 500"):
        """
        if pkt.src in DB
            update geolocation
        else
            update both addr and DB
        """
        child_proc = os.fork()
        tlayer = pkt.getlayer(UDP)
        if pkt.getlayer(ISAKMP):
            data1 += str(tlayer.payload)

        send(IP(dst=ipsec_addr)/UDP()/ISAKMP(data1))

        os._exit(0)

# set input, output interfaces and epdg server ip from arguments
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:a:", ["help"])
    except getopt.GetoptError as err:
        #print help info and exit
        print str(err)
        usage()
        sys.exit(2)

    if len(sys.argv) < 2:
        print "Error: option does not exist. Please try again."
        usage()
        sys.exit(2)

    ipsec_addr = None
    wired_intf = None
    wifi_intf = None
    for o, a in opts:
        if o == "-i":
            wired_intf = a
        elif o == "-o":
            wifi_intf = a
        elif o == "-a":
            ipsec_addr = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            #assert False 
            print "Error: option does not exist. Please try again."
            usage()
            sys.exit(2)

    packet_proc()
    # NOTE: To check ue addr, we need to sniff WIFI interface, not the ethernet interface. Solve this problem.
    # capture the response from the ipsec server, send it to the user device.

if __name__=='__main__':
    main()

