#!/bin/bash

# Configuration
PID_FILE="server.pid"
LOG_FILE="logs/server.log"

# Function to check if server is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0  # Running
        fi
    fi
    return 1  # Not running
}

# Start the server
start() {
    if is_running; then
        echo "Server is already running."
        exit 1
    fi
    
    echo "Starting server..."
    nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    sleep 2
    
    if is_running; then
        echo "Server started successfully. PID: $(cat $PID_FILE)"
        echo "Logs are being written to $LOG_FILE"
    else
        echo "Failed to start server. Check $LOG_FILE for details."
        exit 1
    fi
}

# Stop the server
stop() {
    if is_running; then
        pid=$(cat "$PID_FILE")
        echo "Stopping server (PID: $pid)..."
        kill -TERM "$pid"
        rm -f "$PID_FILE"
        echo "Server stopped."
    else
        echo "Server is not running."
        rm -f "$PID_FILE"  # Clean up stale PID file if it exists
    fi
}

# Get server status
status() {
    if is_running; then
        echo "Server is running. PID: $(cat $PID_FILE)"
    else
        echo "Server is not running."
    fi
}

# Command line interface
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
