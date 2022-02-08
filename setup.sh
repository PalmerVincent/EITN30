#!/bin/bash

# Setting up RPi


# address="inutiuser@inuti$nbr.lab.eit.lth.se"
repo="git@github.com:PalmerVincent/EITN30.git"
pass="LangGeNot5G"

# Configure git 

git config --global user.email "notmy@email.com"
git config --global user.name "InternetInutiPi"

# Installing repo


if [[ -f "~/git/" ]]
then
    if [[ -f "~/git/EITN30/.git" ]]
    then
        echo "Repo exists, updating."
        cd ~/git/EITN30
        git pull
    else
        echo "Repo missing, cloning."
        cd ~/git/
        git clone $repo
    fi
else
    echo "Directory missing. Creating and cloning repo."
    mkdir ~/git
    cd ~/git
    git clone $repo
fi


# Installing dependancies

if [[ -f "/usr/include/RF24/" ]]
then
    echo "Library exists"
else
    cd ~/git/EITN30/
    wget "https://github.com/nRF24/RF24/releases/download/v1.4.2/librf24-RPi_1.4.2-1_armhf.deb"
    sudo dpkg -i librf24-RPi*armhf.deb
    rm librf24-RPi*armhf.deb
    echo "Library is installed"
fi

echo $pass | sudo -S apt-get install python3-dev libboost-python-dev python3-pip python3-rpi.gpio build-essentials

python3 -m pip install --upgrade pip setuptools


echo $pass | sudo -S ln -s $(ls /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3*.so | tail -1) /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3.so


# Navigating for cloning repo, building wrapper

cd ~/git/EITN30/

git clone https://github.com/nRF24/RF24.git

cd RF24/pyRF24/

python3 setup.py build

echo "Build complete"

sudo python3 setup.py install

echo "Install complete"


