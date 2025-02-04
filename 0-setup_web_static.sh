#!usr/bin/env bash
# Exit on any error
set -e

# Install Nginx if not already installed
if ! dpkg -l | grep -q nginx; then
  echo "Installing Nginx..."
  apt-get update
  apt-get install -y nginx
fi

# Create necessary directories
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

# Create a fake HTML file for testing
cat << EOF > /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Create symbolic link
if [ -L /data/web_static/current ]; then
  rm /data/web_static/current
fi
ln -s /data/web_static/releases/test /data/web_static/current

# Set ownership of /data/ folder to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
CONFIG_FILE="/etc/nginx/sites-available/default"

if ! grep -q "location /hbnb_static/" "$CONFIG_FILE"; then
  echo "Updating Nginx configuration..."
  sed -i '/server_name _;/a \
    location /hbnb_static/ {
        alias /data/web_static/current/;
    }' "$CONFIG_FILE"
fi

# Restart Nginx
service nginx restart

# Exit successfully
echo "Setup complete!"

