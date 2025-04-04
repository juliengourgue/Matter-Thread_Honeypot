#!/bin/bash
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
GIT_ROOT="$(git rev-parse --show-toplevel)"

MONITORING_VENV="$GIT_ROOT/monitoring/venv"

# Check if the virtual environment exists
if sudo [ ! -d "$MONITORING_VENV" ]; then
    echo "The initilisation of the HoneyPot is not done : venv does't exist"
    exit 1
fi
source $MONITORING_VENV/bin/activate

echo "Starting the Monitoring server on Port 5000 of the current host"
$MONITORING_VENV/bin/python3 monitoring/app.py

echo "Starting the network monitoring..."
rm -f monitoring/stop_signal.txt
touch  monitoring/stop_signal.txt
nohup sudo  $MONITORING_VENV/bin/python3 monitoring/network_monitoring.py --name "network_monitor" & 
