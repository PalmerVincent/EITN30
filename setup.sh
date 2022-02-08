#!/bin/bash

# Setting up RPi


# address="inutiuser@inuti$nbr.lab.eit.lth.se"
repo="git@github.com:PalmerVincent/EITN30.git"
pass="LangGeNot5G"

# Configure git 

git config --global user.email "notmy@email.com"
git config --global user.name "InternetInutiPi"


# Installing dependencies
echo $pass | sudo -s apt-get update
echo $pass | sudo -s apt-get upgrade 

echo $pass | sudo pip3 install Adafruit-Blinka
echo $pass | sudo pip3 install circuitpython-nrf24l01

clear
echo "Done with setup!"
