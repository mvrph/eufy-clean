#!/bin/bash
# Setup virtual environment and install dependencies

echo "=========================================="
echo "Setting up virtual environment..."
echo "=========================================="
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install aiohttp paho-mqtt protobuf python-dotenv

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "To use the library:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Create .env file with your credentials:"
echo "     ./create_env.sh"
echo ""
echo "  3. Run the example:"
echo "     python3 standalone_example.py"
echo ""
