#!/bin/bash

echo 'Setting up Yggdrasil environment...'
python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo 'Ready. Add your API keys to .env.'
