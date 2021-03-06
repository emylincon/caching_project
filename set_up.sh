#!/bin/bash

clear
echo 'preparing your MEC Caching Platform'
sleep 3
apt update && apt upgrade -y
apt install python3 -y
apt install python3-pip -y
pip3 install drawnow -y
apt install python3-psutil -y
apt install python3-matplotlib -y
apt install python3-paramiko -y
apt install python3-pyfiglet -y
apt install python3-sqlite3 -y
apt install openssh-client -y
apt install openssh-server -y
apt install wget -y
apt install curl -y
apt install man -y
apt install apt-utils -y
apt install iputils-ping -y
apt install net-tools -y
apt install nano -y
apt install iperf3 -y
apt install python3-numpy -y
apt install nmap -y


mv * ..
python3 /home/mec/files_cache/refresh_db.py
/etc/init.d/ssh start
clear
echo 'All done.. Ready to use!'
