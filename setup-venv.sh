#!/bin/bash

#Delete the existing .venv directory
VENV=".venv"
if [ -d "$VENV" ]; then
  echo "$VENV exists. Deleting..."
  rm -rf "$VENV"
fi

#Create a new virtual environment
python3 -m venv .venv

#Activate the virtual environment
source .venv/bin/activate

#Install the required packages
pip install -e ".[dev]"