#!/bin/bash
echo Server wird in 3s gestartet...
sleep 3
cd /home/pi/ServerFiles/Server
python3 Server.py
cd /
