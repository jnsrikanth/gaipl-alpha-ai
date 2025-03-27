#!/bin/bash

# Check if manage_server.sh exists and has proper permissions
if [ -f "manage_server.sh" ]; then
    echo "manage_server.sh already exists."
    
    # Check if it's executable
    if [ -x "manage_server.sh" ]; then
        echo "Script is executable."
    else
        echo "Making script executable..."
        chmod +x manage_server.sh
    fi
    
    # Display current server status
    ./manage_server.sh status
else
    echo "manage_server.sh does not exist in the current directory."
    echo "Please verify the correct location of the script."
fi

