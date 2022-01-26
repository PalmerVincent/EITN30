#!/bin/bash

# Setup

echo "What is the Pi number?"
read nbr

address="inutiuser@inuti$nbr.lab.eit.lth.se"
repo="git@github.com:PalmerVincent/EITN30.git"

# Copy key to Pi 

ssh-copy-id -i ~/.ssh/eitn30-pi.pub $address

# Start ssh

# echo "LangGeNot5G" | ssh $address 

# Configure git 

# git config --global user.email "vincent.palmer@hotmail.com"
# git config --global user.name "InternetInuti"

# Fix Git repo

# if [ -d "~/EITN30" ]
# then 
#	echo "Repo exists, Updating"
#	cd ~/EITN30
#	git pull
# else
#	echo "Repo missing, Cloning"
#	git clone $repo

# fi

# cd ~/EITN30

# Installing dependencies


