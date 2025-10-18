#!/bin/bash

# GCP Compute Engine Deployment Script
# Run this script on your local machine to set up the GCP infrastructure

set -e

# Configuration
PROJECT_ID="your-project-id"
INSTANCE_NAME="buildbuzz-backend"
ZONE="us-central1-a"
MACHINE_TYPE="e2-medium"
IMAGE_FAMILY="ubuntu-2204-lts"
IMAGE_PROJECT="ubuntu-os-cloud"
DISK_SIZE="20GB"
STARTUP_SCRIPT="startup.sh"

echo "Starting GCP Compute Engine deployment..."

# Ensure you're logged into gcloud
echo "Checking gcloud authentication..."
gcloud auth list

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable compute.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com

# Create firewall rule for HTTP traffic
echo "Creating firewall rules..."
gcloud compute firewall-rules create allow-http-buildbuzz \
    --allow tcp:80 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow HTTP traffic for BuildBuzz Backend" \
    --target-tags http-server || echo "Firewall rule already exists"

# Create firewall rule for HTTPS traffic
gcloud compute firewall-rules create allow-https-buildbuzz \
    --allow tcp:443 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow HTTPS traffic for BuildBuzz Backend" \
    --target-tags https-server || echo "Firewall rule already exists"

# Create the Compute Engine instance
echo "Creating Compute Engine instance..."
gcloud compute instances create $INSTANCE_NAME \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --network-interface=network-tier=PREMIUM,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=$(gcloud config get-value account) \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=$INSTANCE_NAME,image=projects/$IMAGE_PROJECT/global/images/family/$IMAGE_FAMILY,mode=rw,size=$DISK_SIZE,type=projects/$PROJECT_ID/zones/$ZONE/diskTypes/pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --reservation-affinity=any \
    --metadata-from-file startup-script=$STARTUP_SCRIPT

echo "Instance created successfully!"

# Get the external IP
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "================================================"
echo "Deployment Information:"
echo "================================================"
echo "Instance Name: $INSTANCE_NAME"
echo "Zone: $ZONE"
echo "External IP: $EXTERNAL_IP"
echo "Application URL: http://$EXTERNAL_IP"
echo ""
echo "To connect via SSH:"
echo "gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo ""
echo "To check application logs:"
echo "gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo journalctl -u buildbuzz-backend -f'"
echo ""
echo "To update the application:"
echo "gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo systemctl stop buildbuzz-backend && cd /opt/buildbuzz/backend && sudo -u buildbuzz git pull origin sagar-test-users && sudo -u buildbuzz /opt/buildbuzz/backend/venv/bin/pip install -r requirements.txt && sudo systemctl start buildbuzz-backend'"
echo "================================================"

echo "Waiting for instance to be ready..."
sleep 60

echo "Checking application status..."
curl -f http://$EXTERNAL_IP/health || echo "Application may still be starting up. Check logs if this persists."

echo "Deployment completed!"