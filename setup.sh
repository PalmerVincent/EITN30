#!/bin/bash

# Setting up RPi


# address="inutiuser@inuti$nbr.lab.eit.lth.se"
repo="git@github.com:PalmerVincent/EITN30.git"
pass="LangGeNot5G"

# Configure git 

git config --global user.email "notmy@email.com"
git config --global user.name "InternetInutiPi"

# Installing repo

echo $repofolder

if [[ -f "$HOME/git/" ]]
then
    if [[ -f "$HOME/git/EITN30/.git" ]]
    then
        echo "Git repository exists, updating."
        cd $HOME/git/$repofolder/
        git pull
    else
        echo "Git repository missing, cloning."
        cd $HOME/git/
        git clone $repository
    fi
else

    echo "Git directory missing. Creating and cloning repository."
    mkdir $HOME/git/
    cd $HOME/git/
    git clone $repository
fi