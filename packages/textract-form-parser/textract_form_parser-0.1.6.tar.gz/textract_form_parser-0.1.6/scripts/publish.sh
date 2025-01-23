#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install required packages
pip install --upgrade build twine python-dotenv

# Run the publish script
python scripts/publish.py
