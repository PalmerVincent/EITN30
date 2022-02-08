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
