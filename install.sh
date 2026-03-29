#!/usr/bin/env bash

# Ultimate WordPress Manager Installer
# Install by running: curl -sSL https://raw.githubusercontent.com/ehtishamnaveed/wordpress-manager/master/install.sh | bash

set -e

INSTALL_DIR="$HOME/.local/bin"
SCRIPT_NAME="wordpress"

echo "🚀 Installing Ultimate WordPress Manager..."

# Create local bin if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Download the script (or copy from local if in repo)
if [ -f "./wordpress.py" ]; then
    cp ./wordpress.py "$INSTALL_DIR/$SCRIPT_NAME"
else
    # Fallback to GitHub download
    curl -sSL "https://raw.githubusercontent.com/ehtishamnaveed/wordpress-manager/master/wordpress.py" -o "$INSTALL_DIR/$SCRIPT_NAME"
fi

chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

echo "✅ Success! Installed to $INSTALL_DIR/$SCRIPT_NAME"
echo ""
echo "Please ensure $INSTALL_DIR is in your PATH."
echo "You can now run: wordpress list"
