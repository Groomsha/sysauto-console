#!/bin/bash

ip link set dev wlp1s0 down
iwconfig wlp1s0 mode monitor

macchanger -r wlp1s0
ip link set dev wlp1s0 up

airmon-ng check kill
airodump-ng wlp1s0
