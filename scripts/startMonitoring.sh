#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
GIT_ROOT="$(git rev-parse --show-toplevel)"

MONITORING_VENV="$GIT_ROOT/monitoring/venv"

# Check if the virtual environment exists
if sudo [ ! -d "$MONITORING_VENV" ]; then
    echo "The initialisation of the HoneyPot is not done : venv doesn't exist"
    exit 1
fi

MONITORING=$GIT_ROOT/monitoring

echo "Starting the Monitoring server on Port 5000 of the current host"
$MONITORING_VENV/bin/python3 $MONITORING/app.py &> /dev/null &

# Capture the PID of the Flask app and save it to a file
FLASK_APP_PID=$!
echo $FLASK_APP_PID > flask_app_pid.txt

echo "Starting the network monitoring..."
sudo $MONITORING_VENV/bin/python3 $MONITORING/network_monitoring.py &> /dev/null &

# Capture the PID of the network monitor and save it to a file
NETWORK_MONITOR_PID=$!
echo $NETWORK_MONITOR_PID > network_monitor_pid.txt

echo "Both Flask app and network monitor started successfully!"
