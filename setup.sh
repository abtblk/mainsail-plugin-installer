#!/bin/bash

echo "Installing dependencies..."
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install flask

echo "Starting server at http://mainsail.local:5010 or http://<pi-ip>:5010"
python3 app.py
