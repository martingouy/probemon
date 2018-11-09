#!/usr/bin/env bash
# Set environment variable
echo "AP_ID="$1 >> /etc/environment

# Automated login on root
cp ./lightdm-autologin /etc/pam.d/lightdm-autologin
cp ./lightdm.conf /etc/lightdm/lightdm.conf

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


# Install supervisor
apt-get update
apt-get install -y supervisor
mkdir /var/log/webhook
cp /root/sniffing/probemon/setup_files/supervisord.conf /etc/supervisor/
echo "environment=AP_ID="$1 >> /etc/supervisor/supervisord.conf
systemctl enable supervisor
systemctl start supervisor

#supervisord
#systemctl enable supervisor
#systemctl start supervisor
#cp /root/sniffing/probemon/setup_files/pythonhook.conf /etc/supervisor/conf.d/
#echo "environment=AP_ID="$1 >> /etc/supervisor/conf.d/pythonhook.conf
#supervisorctl reread
#supervisorctl update

## Restart
#/sbin/shutdown -h now
