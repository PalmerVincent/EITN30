#!/bin/bash

# Setting up RPi


# address="inutiuser@inuti$nbr.lab.eit.lth.se"
repo="git@github.com:PalmerVincent/EITN30.git"


# Configure git 

git config --global user.email "vincent.palmer@hotmail.com"
git config --global user.name "InternetInuti"


# Installing dependencies
#echo -e "LangGeNot5G" | sudo apt-get update
#sudo apt-get upgrade 

echo -e "LangGeNot5G" | sudo pip3 install Adafruit-Blinka
pip3 install circuitpython-nrf24l01


echo "Done with setup!"
