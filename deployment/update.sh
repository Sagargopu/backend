#!/bin/bash

# Update and Deploy Script
# Run this on the GCP instance to update the application

set -e

echo "Updating BuildBuzz Backend..."

# Stop the service
sudo systemctl stop buildbuzz-backend

# Switch to application user and update
sudo -u buildbuzz bash << 'EOF'
cd /opt/buildbuzz/backend

# Pull latest changes
git pull origin sagar-test-users

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Run any migrations if needed
# python -m alembic upgrade head

echo "Application updated successfully"
EOF

# Start the service
sudo systemctl start buildbuzz-backend

# Check status
echo "Checking service status..."
sudo systemctl status buildbuzz-backend --no-pager

echo "Update completed!"
echo "Check logs with: sudo journalctl -u buildbuzz-backend -f"