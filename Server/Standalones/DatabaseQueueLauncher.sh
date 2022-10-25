#!/bin/bash
echo DBQueue wird in 3s gestartet...
sleep 3
cd /home/pi/ServerFiles/Server/Standalones
python3 DatabaseQueue.py
cd /
