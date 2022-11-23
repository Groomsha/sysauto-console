#!/bin/bash

ip link set dev wlp1s0 down
macchanger -r wlp1s0
ip link set dev wlp1s0 up

ip link set dev enp0s31f6 down
macchanger -r enp0s31f6
ip link set dev enp0s31f6 up
