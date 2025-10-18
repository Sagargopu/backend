#!/bin/bash

# GCP Compute Engine Startup Script for FastAPI Backend
# This script will run when the VM starts up

set -e

echo "Starting FastAPI Backend deployment..."

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3.11 and essential packages
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip
sudo apt-get install -y nginx supervisor git curl

# Create application user
sudo useradd --system --shell /bin/bash --home /opt/buildbuzz --create-home buildbuzz

# Create application directory
sudo mkdir -p /opt/buildbuzz/backend
sudo chown buildbuzz:buildbuzz /opt/buildbuzz/backend

# Switch to application user for the rest of the setup
sudo -u buildbuzz bash << 'EOF'
cd /opt/buildbuzz

# Clone the repository (you'll need to update this with your actual repo)
if [ ! -d "backend/.git" ]; then
    git clone https://github.com/Sagargopu/backend.git backend
else
    cd backend
    git pull origin sagar-test-users
    cd ..
fi

cd backend

# Create Python virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install additional production dependencies
pip install gunicorn uvicorn[standard] psycopg2-binary

echo "Application setup completed for user buildbuzz"
EOF

# Create systemd service file
sudo tee /etc/systemd/system/buildbuzz-backend.service > /dev/null << 'EOF'
[Unit]
Description=BuildBuzz FastAPI Backend
After=network.target

[Service]
User=buildbuzz
Group=buildbuzz
WorkingDirectory=/opt/buildbuzz/backend
Environment=PATH=/opt/buildbuzz/backend/venv/bin
EnvironmentFile=/opt/buildbuzz/backend/.env
ExecStart=/opt/buildbuzz/backend/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create nginx configuration
sudo tee /etc/nginx/sites-available/buildbuzz-backend > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/buildbuzz-backend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable buildbuzz-backend
sudo systemctl enable nginx

# Start services
sudo systemctl start nginx
sudo systemctl start buildbuzz-backend

# Check service status
echo "Service Status:"
sudo systemctl status buildbuzz-backend --no-pager
sudo systemctl status nginx --no-pager

echo "Deployment completed!"
echo "Application should be accessible on port 80"
echo "Check logs with: sudo journalctl -u buildbuzz-backend -f"