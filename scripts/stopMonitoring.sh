#!/bin/bash
echo "Stopping the network monitoring..."
echo "It will take 1min to be sure that the current data are saved before stopping"
echo "STOP" >  monitoring/stop_signal.txt  # Writing STOP to the file
sleep 60
sudo pkill -f "network_monitor"
