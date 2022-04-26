#!/bin/sh
source ./server/bin/activate
brew services start mongodb-community@5.0
python3 main.py
