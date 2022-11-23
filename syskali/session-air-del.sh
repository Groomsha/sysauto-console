#!/bin/bash

ip link set dev wlp1s0 down
iwconfig wlp1s0 mode managed

macchanger -r wlp1s0
ip link set dev wlp1s0 up

service NetworkManager stop
service NetworkManager start

echo '' > /root/.bash_history
echo '' > /home/groomsha/.bash_history
