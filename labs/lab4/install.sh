# SUTD 50.012 
# Install mininet and supporting libraries
sudo apt -y install mininet
# Install curl package for pip3.4 installation
sudo apt install curl
# Install pip3.4
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3.4 get-pip.py
# Install matplotlib package for lab4 plotting figures
# If occur 'cannot uninstall six', try adding the flags --ignore-installed six
# sudo pip3.4 install matplotlib --ignore-installed six
sudo pip3.4 install matplotlib
