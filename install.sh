#!/bin/bash

sudo apt  update -y &&sudo  apt install  tor -y

if pip3 install  -r requirements.txt; then
echo "reqirements was installled"
else 
pip3 install -r requirements.txt --break-system-packages
echo  "reqirements was installled"
fi

cd ..
sudo cp -r torsearch/ /opt/torsearch

sudo ln -s /opt/torsearch/searcher.py /usr/local/bin/searcher
sudo chmod +x /opt/torsearch/searcher.py
sudo rm -rf  torsearch
cd ~
echo "The installation was completed!"
echo"Please input  in terminal: torsearch --help"
