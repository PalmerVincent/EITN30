#!/bin/bash

# Script for pushing changes to repo and removing local files on RPi

git add .
git commit -m "Commit before cleaning"
git push
 
cd ..
rm -rf EITN30

source exit



