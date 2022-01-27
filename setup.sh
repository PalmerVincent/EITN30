#!/bin/bash

# Setting up RPi


# address="inutiuser@inuti$nbr.lab.eit.lth.se"
repo="git@github.com:PalmerVincent/EITN30.git"
pipe="echo LangGeNot5G |"

# Configure git 

git config --global user.email "vincent.palmer@hotmail.com"
git config --global user.name "InternetInuti"


# Installing dependencies
$pipe sudo -s apt-get update
$pipe sudo -s apt-get upgrade 

$pipe sudo pip3 install Adafruit-Blinka
$pipe sudo pip3 install circuitpython-nrf24l01


echo "Done with setup!"
