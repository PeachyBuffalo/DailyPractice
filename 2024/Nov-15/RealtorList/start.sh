#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install or upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Start Gunicorn server
gunicorn --config gunicorn_config.py wsgi:app 