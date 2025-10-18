#!/bin/bash

# Cloud SQL Setup Script
# Run this to create and configure Cloud SQL PostgreSQL instance

set -e

# Configuration
PROJECT_ID="your-project-id"
INSTANCE_NAME="buildbuzz-db"
REGION="us-central1"
DATABASE_NAME="buildbuzz"
USER_NAME="buildbuzz_user"
MACHINE_TYPE="db-f1-micro"  # Change to db-n1-standard-1 for production

echo "Setting up Cloud SQL PostgreSQL instance..."

# Create Cloud SQL instance
echo "Creating Cloud SQL instance..."
gcloud sql instances create $INSTANCE_NAME \
    --database-version=POSTGRES_14 \
    --tier=$MACHINE_TYPE \
    --region=$REGION \
    --storage-type=SSD \
    --storage-size=10GB \
    --storage-auto-increase \
    --backup-start-time=02:00 \
    --enable-bin-log \
    --maintenance-window-day=SUN \
    --maintenance-window-hour=3 \
    --maintenance-release-channel=production \
    --deletion-protection

echo "Cloud SQL instance created successfully!"

# Set root password
echo "Setting root password..."
gcloud sql users set-password postgres \
    --instance=$INSTANCE_NAME \
    --password=$(openssl rand -base64 32)

# Create database
echo "Creating database..."
gcloud sql databases create $DATABASE_NAME --instance=$INSTANCE_NAME

# Create user
echo "Creating database user..."
USER_PASSWORD=$(openssl rand -base64 32)
gcloud sql users create $USER_NAME \
    --instance=$INSTANCE_NAME \
    --password=$USER_PASSWORD

# Get connection information
CONNECTION_NAME=$(gcloud sql instances describe $INSTANCE_NAME --format='value(connectionName)')
EXTERNAL_IP=$(gcloud sql instances describe $INSTANCE_NAME --format='value(ipAddresses[0].ipAddress)')

echo "================================================"
echo "Cloud SQL Setup Complete!"
echo "================================================"
echo "Instance Name: $INSTANCE_NAME"
echo "Connection Name: $CONNECTION_NAME"
echo "External IP: $EXTERNAL_IP"
echo "Database Name: $DATABASE_NAME"
echo "Username: $USER_NAME"
echo "Password: $USER_PASSWORD"
echo ""
echo "Connection Strings:"
echo "Cloud SQL Proxy: postgresql://$USER_NAME:$USER_PASSWORD@/$DATABASE_NAME?host=/cloudsql/$CONNECTION_NAME"
echo "External IP: postgresql://$USER_NAME:$USER_PASSWORD@$EXTERNAL_IP:5432/$DATABASE_NAME"
echo ""
echo "Add this to your .env file:"
echo "DATABASE_URL=postgresql://$USER_NAME:$USER_PASSWORD@/$DATABASE_NAME?host=/cloudsql/$CONNECTION_NAME"
echo "================================================"

# Save credentials to file
cat > cloud-sql-credentials.txt << EOF
Instance Name: $INSTANCE_NAME
Connection Name: $CONNECTION_NAME
External IP: $EXTERNAL_IP
Database Name: $DATABASE_NAME
Username: $USER_NAME
Password: $USER_PASSWORD

Cloud SQL Proxy Connection:
DATABASE_URL=postgresql://$USER_NAME:$USER_PASSWORD@/$DATABASE_NAME?host=/cloudsql/$CONNECTION_NAME

External IP Connection:
DATABASE_URL=postgresql://$USER_NAME:$USER_PASSWORD@$EXTERNAL_IP:5432/$DATABASE_NAME
EOF

echo "Credentials saved to cloud-sql-credentials.txt"
echo "IMPORTANT: Store these credentials securely and delete this file after copying to your .env"