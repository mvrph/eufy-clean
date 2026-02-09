#!/bin/bash
echo "Creating .env file template..."
echo ""
echo "Please enter your Eufy credentials:"
read -p "Eufy Username (email): " username
read -sp "Eufy Password: " password
echo ""
echo ""
cat > .env << EOL
EUFY_USERNAME=${username}
EUFY_PASSWORD=${password}
EOL
echo "✅ .env file created!"
