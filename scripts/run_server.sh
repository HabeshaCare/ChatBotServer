#!/bin/bash

echo "Activating Virtual environment"
source Backend/bin/activate

echo "Starting the server..."

gunicorn -c gunicorn.conf.py --bind 0.0.0.0:5000 --reload
