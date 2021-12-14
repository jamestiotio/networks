#!/bin/bash
# Install script for 50.012 exercise 6

# Might need to do some extra workaround if `systemd-resolved` is present due to conflict over port 53
sudo apt-get install dnsmasq #isc-dhcp-server #netstat-nat

#echo 'INTERFACES="srv1-eth0"' | sudo tee /etc/default/isc-dhcp-server
#sudo cp dhcpd.conf /etc/dhcp/
