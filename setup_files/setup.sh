#!/usr/bin/env bash
# Set environment variable
echo "AP_ID="$1 >> /etc/environment

# Copy startup bash script test
cp ./startup.sh ~/startup.sh
cp ./initstartup /etc/init.d/
chmod 755 /etc/init.d/initstartup
update-rc.d initstartup defaults


# Automated login on root 
cp ./lightdm-autologin /etc/pam.d/lightdm-autologin
cp ./lightdm.conf /etc/lightdm/lightdm.conf

# Install supervisor
apt-get update
apt-get install -y supervisor
mkdir /var/log/webhook
# Install python dependencies
cd ~
git clone https://github.com/drkjam/netaddr
cd netaddr
sudo python setup.py install
cd ~
git clone https://github.com/secdev/scapy.git
cd scapy
sudo python setup.py install

# Pull sniffing files
mkdir ~/sniffing 
cd ~/sniffing
git clone https://github.com/martingouy/probemon.git

# Restart
/sbin/shutdown -h now
