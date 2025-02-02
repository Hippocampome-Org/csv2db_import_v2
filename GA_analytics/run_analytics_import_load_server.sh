#!/bin/bash 

PYTHON_EXEC="/usr/bin/python3.7"  # Set the correct Python version
PYTHON_SCRIPT="/var/www/html/csv2db/GA_analytics/import_load.py"
LOG_FILE="/var/log/GA4analytics/error.log"

if [ ! -x "$PYTHON_SCRIPT" ]; then
    echo "ERROR: The script is not executable. Please check the file permissions."
    exit 1
fi

echo "Starting the import process ..." 
output=$($PYTHON_EXEC "$PYTHON_SCRIPT" 2>&1)
exit_status=$?

echo "$output"

if [ $exit_status -eq 0 ]; then
    echo "Import process completed successfully."
else
    echo "Import process failed. Check the logs for errors."
    echo "$output" >> "$LOG_FILE"
    exit 1
fi
