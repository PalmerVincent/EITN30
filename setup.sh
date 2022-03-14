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
    if [[ -d "~/git/EITN30/.git" ]]
    then
        echo "Repo exists, updating."
        echo ""
        cd ~/git/EITN30
        git pull
    else
        echo "Repo missing, cloning."
        echo ""
        cd ~/git/
        git clone $repo
    fi
else
    echo "Directory missing. Creating and cloning repo."
    echo ""
    mkdir ~/git
    cd ~/git
    git clone $repo
fi

echo "Configring nano"
echo ""
echo ""
cp ~/git/EITN30/.nanorc ~/.nanorc


if [[ -f "/usr/local/lib/librf24*" ]]
then
    echo $pass | sudo -S rm -r /usr/local/lib/librf24*
fi

if [[ -d "/usr/local/include/RF24/" ]]
then
    sudo rm -r /usr/local/include/RF24*
fi



cd ~/git/EITN30/


#chmod +x install.sh
#./install.sh

echo ""
echo "Installing RF24 Repo..."
echo ""
git clone https://github.com/tmrh20/RF24.git
echo ""
cd RF24
./configure --driver=SPIDEV
cd ..
make -C ./RF24
sudo make install -C ./RF24

echo "Library is installed"
echo ""
echo ""



# Installing dependancies

echo $pass | sudo -S apt-get update
echo $pass | sudo -S apt-get install -y python3-dev libboost-python-dev python3-pip python3-rpi.gpio build-essential

python3 -m pip install --upgrade pip setuptools autopep8 python-pytuntap


if [[ -e "/usr/lib/arm-linux-gnueabihf/libboost_python3.so" ]] 
then
    sudo rm /usr/lib/arm-linux-gnueabihf/libboost_python3.so
fi


sudo ln -s $(ls /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3*.so | tail -1) /usr/lib/$(ls /usr/lib/gcc | tail -1)/libboost_python3.so


# Navigating for cloning repo, building wrapper

cd ~/git/EITN30/RF24/pyRF24/

python3 setup.py build

echo "Build complete"
echo ""
echo ""

sudo python3 setup.py install
 
echo "Install complete"

echo "Setting up Tun device and forwarding"

cd ~/git/EITN30
echo "Enter base for base node: " 
read base


if [[ $base == "base" ]]
then
    echo "You entered $base"
    sudo ip tuntap add mode tun dev longge
    sudo ip addr add 192.168.1.1/24 dev longge
    sudo ip link set dev longge up
    ./routing.sh
else
    echo "You entered not base"
    sudo ip tuntap add mode tun dev longge
    sudo ip addr add 192.168.1.2/24 dev longge
    sudo ip link set dev longge up
    #sudo ip route add default via 192.168.1.1 dev longge
fi
