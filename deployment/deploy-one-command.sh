#!/bin/bash

# One-Command GCP Deployment Script
# Run this from your local terminal to deploy everything to GCP

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration (you can override these with environment variables)
PROJECT_ID="${GCP_PROJECT_ID:-buildbuzz-backend-prod}"
INSTANCE_NAME="${INSTANCE_NAME:-buildbuzz-backend}"
DB_INSTANCE_NAME="${DB_INSTANCE_NAME:-buildbuzz-db}"
ZONE="${GCP_ZONE:-us-central1-a}"
REGION="${GCP_REGION:-us-central1}"
MACHINE_TYPE="${MACHINE_TYPE:-e2-medium}"
DB_MACHINE_TYPE="${DB_MACHINE_TYPE:-db-f1-micro}"

echo -e "${BLUE}🚀 BuildBuzz Backend - One-Command GCP Deployment${NC}"
echo "================================================"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check prerequisites
echo -e "${BLUE}🔍 Checking prerequisites...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    print_error "Google Cloud SDK (gcloud) is not installed"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    print_warning "Not authenticated with Google Cloud"
    echo "Running: gcloud auth login"
    gcloud auth login
fi

print_status "Prerequisites checked"

# Prompt for configuration if not set
if [ -z "$GCP_PROJECT_ID" ]; then
    echo -n "Enter your GCP Project ID: "
    read PROJECT_ID
fi

echo -e "${BLUE}📋 Deployment Configuration:${NC}"
echo "  Project ID: $PROJECT_ID"
echo "  Instance: $INSTANCE_NAME"
echo "  Database: $DB_INSTANCE_NAME"
echo "  Zone: $ZONE"
echo "  Region: $REGION"
echo ""

# Confirm deployment
echo -n -e "${YELLOW}Do you want to proceed with deployment? (y/N): ${NC}"
read -r confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    print_info "Deployment cancelled"
    exit 0
fi

# Set project
print_info "Setting GCP project to $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable APIs
print_info "Enabling required APIs..."
gcloud services enable compute.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com

# Create firewall rules
print_info "Creating firewall rules..."
gcloud compute firewall-rules create allow-http-buildbuzz \
    --allow tcp:80 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow HTTP traffic for BuildBuzz Backend" \
    --target-tags http-server 2>/dev/null || print_warning "HTTP firewall rule already exists"

gcloud compute firewall-rules create allow-https-buildbuzz \
    --allow tcp:443 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow HTTPS traffic for BuildBuzz Backend" \
    --target-tags https-server 2>/dev/null || print_warning "HTTPS firewall rule already exists"

# Check if Cloud SQL instance exists
print_info "Checking Cloud SQL instance..."
if gcloud sql instances describe $DB_INSTANCE_NAME 2>/dev/null; then
    print_warning "Cloud SQL instance '$DB_INSTANCE_NAME' already exists"
    DB_EXISTS=true
else
    print_info "Creating Cloud SQL instance..."
    gcloud sql instances create $DB_INSTANCE_NAME \
        --database-version=POSTGRES_14 \
        --tier=$DB_MACHINE_TYPE \
        --region=$REGION \
        --storage-type=SSD \
        --storage-size=10GB \
        --storage-auto-increase \
        --backup-start-time=02:00 \
        --maintenance-window-day=SUN \
        --maintenance-window-hour=3 \
        --maintenance-release-channel=production \
        --deletion-protection
    
    # Set root password
    ROOT_PASSWORD=$(openssl rand -base64 32)
    gcloud sql users set-password postgres \
        --instance=$DB_INSTANCE_NAME \
        --password=$ROOT_PASSWORD
    
    # Create database
    gcloud sql databases create buildbuzz --instance=$DB_INSTANCE_NAME
    
    # Create user
    USER_PASSWORD=$(openssl rand -base64 32)
    gcloud sql users create buildbuzz_user \
        --instance=$DB_INSTANCE_NAME \
        --password=$USER_PASSWORD
    
    DB_EXISTS=false
fi

# Get database connection info
CONNECTION_NAME=$(gcloud sql instances describe $DB_INSTANCE_NAME --format='value(connectionName)')
DB_EXTERNAL_IP=$(gcloud sql instances describe $DB_INSTANCE_NAME --format='value(ipAddresses[0].ipAddress)')

if [ "$DB_EXISTS" = false ]; then
    # Save database credentials
    cat > database-credentials.txt << EOF
=== BuildBuzz Database Credentials ===
Instance Name: $DB_INSTANCE_NAME
Connection Name: $CONNECTION_NAME
External IP: $DB_EXTERNAL_IP
Database Name: buildbuzz
Username: buildbuzz_user
Password: $USER_PASSWORD

Cloud SQL Proxy Connection String:
DATABASE_URL=postgresql://buildbuzz_user:$USER_PASSWORD@/buildbuzz?host=/cloudsql/$CONNECTION_NAME

External IP Connection String:
DATABASE_URL=postgresql://buildbuzz_user:$USER_PASSWORD@$DB_EXTERNAL_IP:5432/buildbuzz
EOF
    print_status "Database credentials saved to database-credentials.txt"
fi

# Create startup script with database URL
print_info "Preparing startup script..."
cat > /tmp/startup-script.sh << 'STARTUP_EOF'
#!/bin/bash
set -e

echo "Starting BuildBuzz Backend deployment on $(date)"

# Update system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip
sudo apt-get install -y nginx supervisor git curl

# Create application user
sudo useradd --system --shell /bin/bash --home /opt/buildbuzz --create-home buildbuzz || true

# Create application directory
sudo mkdir -p /opt/buildbuzz/backend
sudo chown buildbuzz:buildbuzz /opt/buildbuzz/backend

# Switch to application user
sudo -u buildbuzz bash << 'EOF'
cd /opt/buildbuzz

# Clone repository
if [ ! -d "backend/.git" ]; then
    git clone https://github.com/Sagargopu/backend.git backend
else
    cd backend
    git pull origin sagar-test-users
    cd ..
fi

cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn uvicorn[standard] psycopg2-binary

echo "Application setup completed"
EOF

# Create systemd service
sudo tee /etc/systemd/system/buildbuzz-backend.service > /dev/null << 'SERVICE_EOF'
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
SERVICE_EOF

# Create nginx configuration
sudo tee /etc/nginx/sites-available/buildbuzz-backend > /dev/null << 'NGINX_EOF'
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
NGINX_EOF

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/buildbuzz-backend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and start services
sudo nginx -t
sudo systemctl daemon-reload
sudo systemctl enable buildbuzz-backend nginx
sudo systemctl start nginx

echo "Deployment completed successfully!"
STARTUP_EOF

# Check if instance exists
print_info "Checking Compute Engine instance..."
if gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE 2>/dev/null; then
    print_warning "Instance '$INSTANCE_NAME' already exists"
    echo -n -e "${YELLOW}Do you want to recreate it? This will delete the existing instance! (y/N): ${NC}"
    read -r recreate
    if [[ $recreate =~ ^[Yy]$ ]]; then
        print_info "Deleting existing instance..."
        gcloud compute instances delete $INSTANCE_NAME --zone=$ZONE --quiet
    else
        print_info "Updating existing instance..."
        # Copy startup script and run it
        gcloud compute scp /tmp/startup-script.sh $INSTANCE_NAME:/tmp/startup-script.sh --zone=$ZONE
        gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo bash /tmp/startup-script.sh'
        
        # Get external IP
        EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
        
        print_status "Instance updated successfully!"
        echo -e "${GREEN}🌐 Application URL: http://$EXTERNAL_IP${NC}"
        echo -e "${BLUE}📊 Health Check: http://$EXTERNAL_IP/health${NC}"
        exit 0
    fi
fi

# Create new instance
print_info "Creating Compute Engine instance..."
gcloud compute instances create $INSTANCE_NAME \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --network-interface=network-tier=PREMIUM,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=$INSTANCE_NAME,image=projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts,mode=rw,size=20GB,type=projects/$PROJECT_ID/zones/$ZONE/diskTypes/pd-balanced \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --reservation-affinity=any \
    --metadata-from-file startup-script=/tmp/startup-script.sh

# Get external IP
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

print_status "Instance created successfully!"

# Create environment file
print_info "Creating environment configuration..."
if [ "$DB_EXISTS" = false ]; then
    ENV_DB_URL="postgresql://buildbuzz_user:$USER_PASSWORD@/buildbuzz?host=/cloudsql/$CONNECTION_NAME"
else
    ENV_DB_URL="postgresql://username:password@/buildbuzz?host=/cloudsql/$CONNECTION_NAME"
fi

cat > /tmp/production.env << ENV_EOF
# Production Environment Variables
DATABASE_URL=$ENV_DB_URL
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=$(openssl rand -base64 32)
JWT_SECRET_KEY=$(openssl rand -base64 32)
GOOGLE_CLOUD_PROJECT=$PROJECT_ID
CORS_ORIGINS=["*"]
LOG_LEVEL=INFO
ENV_EOF

# Wait for instance to be ready
print_info "Waiting for instance to be ready..."
sleep 60

# Copy environment file to instance
print_info "Uploading environment configuration..."
gcloud compute scp /tmp/production.env $INSTANCE_NAME:/tmp/.env --zone=$ZONE
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo mv /tmp/.env /opt/buildbuzz/backend/.env && sudo chown buildbuzz:buildbuzz /opt/buildbuzz/backend/.env'

# Start the application service
print_info "Starting application service..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo systemctl start buildbuzz-backend'

# Clean up temporary files
rm -f /tmp/startup-script.sh /tmp/production.env

echo ""
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo "================================================"
echo -e "${BLUE}📋 Deployment Summary:${NC}"
echo "  Project: $PROJECT_ID"
echo "  Instance: $INSTANCE_NAME"
echo "  Zone: $ZONE"
echo "  External IP: $EXTERNAL_IP"
echo ""
echo -e "${GREEN}🌐 Access your application:${NC}"
echo "  Main URL: http://$EXTERNAL_IP"
echo "  Health Check: http://$EXTERNAL_IP/health"
echo "  API Docs: http://$EXTERNAL_IP/docs"
echo ""
echo -e "${BLUE}🔧 Management commands:${NC}"
echo "  SSH: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo "  Logs: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo journalctl -u buildbuzz-backend -f'"
echo "  Status: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo systemctl status buildbuzz-backend'"
echo ""

if [ "$DB_EXISTS" = false ]; then
    echo -e "${YELLOW}⚠️  Database credentials saved to: database-credentials.txt${NC}"
    echo -e "${RED}🔒 Important: Store these credentials securely and delete the file after use!${NC}"
fi

echo ""
print_info "Testing application health..."
sleep 10
if curl -f -s http://$EXTERNAL_IP/health > /dev/null; then
    print_status "Application is healthy and running!"
else
    print_warning "Application may still be starting up. Check logs if this persists."
    echo "  Logs: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo journalctl -u buildbuzz-backend -f'"
fi

echo ""
echo -e "${GREEN}🚀 Deployment complete! Your BuildBuzz backend is now live!${NC}"