#!/bin/bash
echo "Storage Manager wird in 5s gestartet"
sleep 5
cd /home/pi/ServerFiles/StorageManagement/GUI/
python3 StorageManager.py
cd /
