#!/bin/bash

clear
echo 'preparing your MEC Caching Platform'
sleep 3
apt update && apt upgrade -y
apt install -y python3 \
    python3-pip \
    zip \
    openssh-client \
    openssh-server \
    wget \
    curl \
    man \
    apt-utils \
    iputils-ping \
    net-tools \
    nano \
    iperf3 \
    nmap

pip3 install -r requirements.txt

python3 files_cache/refresh_db.py
/etc/init.d/ssh start
echo 'All done.. Ready to use!'
