#!/bin/bash
# @author  Julien Gourgue

# Stop Flask app
if [ -f "flask_app_pid.txt" ]; then
    FLASK_APP_PID=$(cat flask_app_pid.txt)
    
    if ps -p $FLASK_APP_PID > /dev/null; then
        echo "Stopping Flask app with PID $FLASK_APP_PID..."
        kill $FLASK_APP_PID
        rm flask_app_pid.txt
        echo "Flask app stopped."
    else
        echo "Flask app process not found or already stopped."
        rm flask_app_pid.txt
    fi
else
    echo "Flask app is not running or PID file is missing."
fi

# Stop Network Monitor
if [ -f "network_monitor_pid.txt" ]; then
    NETWORK_MONITOR_PID=$(cat network_monitor_pid.txt)
    
    if ps -p $NETWORK_MONITOR_PID > /dev/null; then
        echo "Stopping Network Monitor with PID $NETWORK_MONITOR_PID..."
        sudo kill $NETWORK_MONITOR_PID
        rm network_monitor_pid.txt
        echo "Network Monitor stopped."
    else
        echo "Network Monitor process not found or already stopped."
        rm network_monitor_pid.txt
    fi
else
    echo "Network Monitor is not running or PID file is missing."
fi
