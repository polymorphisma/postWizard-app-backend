#!/bin/bash
set -e

{
    echo "Script started at $(date)"

    /root/.local/bin/poetry install

    #Activate the Poetry virtual environment
    sleep 3

    sudo systemctl daemon-reload
    echo "daemon-reload complete"
    sleep 5

    sudo systemctl enable uvicorn
    echo "uvicorn enabling complete"

    sudo systemctl start uvicorn
    echo "uvicorn start complete"

    echo "Script completed at $(date)"
} >> script_log.txt 2>&1

