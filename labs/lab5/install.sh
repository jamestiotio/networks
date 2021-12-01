#!/bin/bash
# Installation script for 50.012 Networks Lab 5

sudo apt-get install -y quagga curl screen python-setuptools
sudo easy_install termcolor

# Soft-link the conf files to allow students to edit them directly
sudo rm /etc/quagga/*
sudo ln -s $PWD/conf/bgpd-R1.conf /etc/quagga/
sudo ln -s $PWD/conf/bgpd-R2.conf /etc/quagga/
sudo ln -s $PWD/conf/bgpd-R3.conf /etc/quagga/
sudo ln -s $PWD/conf/bgpd-R4.conf /etc/quagga/
sudo ln -s $PWD/conf/zebra-R1.conf /etc/quagga/
sudo ln -s $PWD/conf/zebra-R2.conf /etc/quagga/
sudo ln -s $PWD/conf/zebra-R3.conf /etc/quagga/
sudo ln -s $PWD/conf/zebra-R4.conf /etc/quagga/
sudo chown quagga /etc/quagga/*.conf

# Create /var/run/quagga, which is sometimes mysteriously not created by install
# Without it, zebra will not update host routes
# Note that this folder is ephemeral, so it will be deleted on a hard reboot (re-execute these 2 lines after a reboot)
# Since the routing tables are stored/updated by zebra here, without this folder, inter-AS communication would be impossible (i.e., `Destination Net Unreachable` errors during pings)
sudo mkdir /var/run/quagga
sudo chown quagga /var/run/quagga
