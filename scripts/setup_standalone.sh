#!/bin/bash
# Setup script for standalone usage
# Run this to install all required dependencies

echo "=========================================="
echo "Eufy Clean - Standalone Setup"
echo "=========================================="
echo ""

echo "Installing dependencies..."
python3 -m pip install --user aiohttp paho-mqtt protobuf python-dotenv

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "Next steps:"
echo "1. Create a .env file with your credentials:"
echo "   EUFY_USERNAME=your-email@example.com"
echo "   EUFY_PASSWORD=your-password"
echo ""
echo "2. Run: python3 standalone_example.py"
echo ""
