#!/bin/bash

echo "Setting up virtual environment"
python3 -m venv Backend
source Backend/bin/activate

echo "Installing requirements"
pip install -qr requirements.txt

echo "Setup complete"

# TODO: see how installing dependancies here goes with installing dependancies in the docker file.
