# ePDG Discovery

This folder contains the files used to discover Evolved Packet Data Gateway (ePDG) servers.

The script here performs the following tasks:

- Enumerate through different MNC (Mobile Network Codes) and MCC (Mobile Country Codes) to generate the list of all ePDG servers.

- Validate the existence of each ePDG server through DNS lookups.

- Generate `iptables` commands to block connections to each in our test environment.