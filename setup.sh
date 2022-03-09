#!/bin/bash

# Setting up RPi


# address="inutiuser@inuti$nbr.lab.eit.lth.se"
repo="git@github.com:PalmerVincent/EITN30.git"
pass="LangGeNot5G"

# Configure git 

git config --global user.email "notmy@email.com"
git config --global user.name "InternetInutiPi"
git config --global pull.rebase false

# Installing repo


if [[ -d "~/git/" ]]
then
    if [[ -f "~/git/EITN30/.git" ]]
    then
        echo "Repo exists, updating.\n"
        cd ~/git/EITN30
        git pull
    else
        echo "Repo missing, cloning.\n"
        cd ~/git/
        git clone $repo
    fi
else
    echo "Directory missing. Creating and cloning repo.\n"
    mkdir ~/git
    cd ~/git
    git clone $repo
fi

echo "Configring nano\n\n"
cp ~/git/EITN30/.nanorc ~/.nanorc


if [[ -f "/usr/local/lib/librf24*" ]]
then
    echo $pass | sudo -S rm -r /usr/local/lib/librf24*
fi
cd ~/git/EITN30/
chmod +x install.sh
./install.sh
echo "Library is installed\n\n"



# Installing dependancies

echo $pass | sudo -S apt-get update
echo $pass | sudo -S apt-get install -y python3-dev libboost-python-dev python3-pip python3-rpi.gpio build-essential

python3 -m pip install --upgrade pip setuptools autopep8


if [[ -e "/usr/lib/arm-linux-gnueabihf/libboost_python3.so" ]] 
then
    sudo rm /usr/lib/arm-linux-gnueabihf/libboost_python3.so
fi


sudo ln -s $(ls /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3*.so | tail -1) /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3.so


# Navigating for cloning repo, building wrapper

cd ~/git/EITN30/rf24libs/RF24/pyRF24/

python3 setup.py build

echo "Build complete\n\n"

sudo python3 setup.py install

echo "Install complete"


