#!/usr/bin/env sh

sudo sysctl -w net.ipv4.ip_forward=0
sudo sysctl -w net.ipv4.conf.eth0.forwarding=0
sudo sysctl -w net.ipv6.conf.eth0.forwarding=0

sudo iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
sudo iptables        -D FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo iptables        -D FORWARD -i wlan0 -o eth0 -j ACCEPT
