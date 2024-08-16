#!/bin/bash

# Check if virtual environment exists, create if it doesn't
if [ ! -d "dejaq_env" ]; then
    python3 -m venv dejaq_env
    source dejaq_env/bin/activate
    pip install -e .
else
    source dejaq_env/bin/activate
fi

# Run dejaq with any provided arguments
dejaq "$@"