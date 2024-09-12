#!/bin/bash

# This script runs a Python script to import Google Analytics data into a database.
# It requires elevated privileges.

# Define the path to the Python script
PYTHON_SCRIPT="/var/www/html/csv2db_import_v2/GA_analytics/import_load.py"

# Check if the script has executable permissions
if [ ! -x "$PYTHON_SCRIPT" ]; then
    echo "Error: The script is not executable. Please check the file permissions."
    exit 1
fi

# Execute the Python script with elevated privileges
echo "Starting the import process..."
sudo /usr/bin/python3.7 "$PYTHON_SCRIPT"

# Check the exit status of the last command
if [ $? -eq 0 ]; then
    echo "Import process completed successfully."
else
    echo "Import process failed. Check the logs for errors."
    exit 1
fi
~                                                                               
