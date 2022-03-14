#!/bin/bash

# Script for pushing changes to repo and removing local files on RPi
git pull
git add .
git commit -m "Commit before cleaning"
git push

cd ..
sudo iptables -F
sudo ip link delete longge
sudo rm -rf ~/git ~/setup.sh

echo "Done with clean, type exit to exit ssh connection!"


