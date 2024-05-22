#!/bin/bash

echo "Setting up virtual environment"
echo "Installing requirements"
poetry install

echo "Setup complete"

# TODO: see how installing dependancies here goes with installing dependancies in the docker file.
