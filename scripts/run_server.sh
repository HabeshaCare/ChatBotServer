#!/bin/bash

echo "Activating Virtual environment"
source Backend/bin/activate

echo "Starting the server..."
# python main.py

# gunicorn main:app --worker-class gevent --bind 0.0.0.0:5000 --timeout 180 --reload
gunicorn -c gunicorn.conf.py --bind 0.0.0.0:5000 --reload
