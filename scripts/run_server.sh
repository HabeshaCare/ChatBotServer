#!/bin/bash

echo "Starting the server..."

gunicorn -c gunicorn.conf.py --bind 0.0.0.0:5000 --reload
