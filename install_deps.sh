#!/bin/bash
echo "Installing dependencies..."
pip3 install aiohttp paho-mqtt protobuf python-dotenv
echo ""
echo "✅ Dependencies installed!"
echo ""
echo "Next: Create a .env file with your credentials:"
echo "  EUFY_USERNAME=your-email@example.com"
echo "  EUFY_PASSWORD=your-password"
