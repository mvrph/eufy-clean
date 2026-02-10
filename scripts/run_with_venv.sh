#!/bin/bash
# Run a Python script with the virtual environment activated

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run ./setup_venv.sh first"
    exit 1
fi

source venv/bin/activate
python3 "$@"
