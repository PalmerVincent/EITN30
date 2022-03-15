#!/bin/bash

echo 1 > /proc/sys/net/ipv4/ip_forward

# Forwarding for base
echo "In routing.sh"


sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

sudo iptables -A FORWARD -i eth0 -o longge -m state --state RELATED,ESTABLISHED -j ACCEPT

sudo iptables -A FORWARD -i longge -o eth0 -j ACCEPT
