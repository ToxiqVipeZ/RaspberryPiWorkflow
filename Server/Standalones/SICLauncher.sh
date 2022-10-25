#!/bin/bash
echo SIC wird in 3s gestartet...
sleep 3
cd /home/pi/ServerFiles/Server/Standalones
python3 ShopInformationCollector.py
cd /
