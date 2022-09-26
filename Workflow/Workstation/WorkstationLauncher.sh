#!/bin/bash
echo "Starting WorkstationApp in 10s..."
sleep 10
cd /home/pi/WorkstationApp
python3 WorkstationApp.py
cd /
