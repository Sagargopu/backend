# GCP CLI Deployment - Quick Start Guide

## 🚀 One-Command Deployment

Deploy your entire BuildBuzz backend to Google Cloud Platform with a single command from your terminal!

## Prerequisites

1. **Google Cloud SDK**: Install gcloud CLI
   ```bash
   # Install gcloud (if not installed)
   # Visit: https://cloud.google.com/sdk/docs/install
   
   # Or use package managers:
   # macOS: brew install google-cloud-sdk
   # Ubuntu: sudo apt-get install google-cloud-sdk
   ```

2. **Authentication**: Login to GCP
   ```bash
   gcloud auth login
   ```

3. **Project**: Have a GCP project ready (or create one)
   ```bash
   # Create new project (optional)
   gcloud projects create buildbuzz-backend-prod
   
   # Enable billing (required)
   # Visit: https://console.cloud.google.com/billing
   ```

## 🎯 Deploy Everything in One Command

### Option 1: Interactive Deployment
```bash
# Make script executable
chmod +x deployment/deploy-one-command.sh

# Run deployment (will prompt for project ID)
./deployment/deploy-one-command.sh
```

### Option 2: Automated Deployment with Environment Variables
```bash
# Set your configuration
export GCP_PROJECT_ID="your-project-id"
export GCP_ZONE="us-central1-a"
export INSTANCE_NAME="buildbuzz-backend"

# Deploy
./deployment/deploy-one-command.sh
```

### Option 3: Command Line Arguments
```bash
GCP_PROJECT_ID="your-project-id" ./deployment/deploy-one-command.sh
```

## 📋 What Gets Deployed

The one-command script will:

1. ✅ **Enable required APIs** (Compute Engine, Cloud SQL)
2. ✅ **Create firewall rules** (HTTP/HTTPS traffic)
3. ✅ **Deploy Cloud SQL PostgreSQL** database
4. ✅ **Launch Compute Engine** instance
5. ✅ **Install and configure** your FastAPI application
6. ✅ **Set up Nginx** reverse proxy
7. ✅ **Configure systemd** service for auto-restart
8. ✅ **Generate secure passwords** and environment variables
9. ✅ **Test application** health

## 🔧 Post-Deployment Management

Use the management script for ongoing operations:

```bash
# Make management script executable
chmod +x deployment/manage.sh

# Check application status
./deployment/manage.sh status

# View live logs
./deployment/manage.sh logs

# Update application (pull latest code)
./deployment/manage.sh update

# Restart application
./deployment/manage.sh restart

# Get external IP and URLs
./deployment/manage.sh ip

# SSH into instance
./deployment/manage.sh ssh

# Check application health
./deployment/manage.sh health
```

## 📊 Example Deployment Session

```bash
$ ./deployment/deploy-one-command.sh

🚀 BuildBuzz Backend - One-Command GCP Deployment
================================================
🔍 Checking prerequisites...
✅ Prerequisites checked

📋 Deployment Configuration:
  Project ID: buildbuzz-backend-prod
  Instance: buildbuzz-backend
  Database: buildbuzz-db
  Zone: us-central1-a
  Region: us-central1

⚠️  Do you want to proceed with deployment? (y/N): y

ℹ️  Setting GCP project to buildbuzz-backend-prod
ℹ️  Enabling required APIs...
ℹ️  Creating firewall rules...
ℹ️  Creating Cloud SQL instance...
ℹ️  Creating Compute Engine instance...
ℹ️  Waiting for instance to be ready...
ℹ️  Starting application service...

🎉 Deployment completed successfully!
================================================
📋 Deployment Summary:
  Project: buildbuzz-backend-prod
  Instance: buildbuzz-backend
  Zone: us-central1-a
  External IP: 34.123.45.67

🌐 Access your application:
  Main URL: http://34.123.45.67
  Health Check: http://34.123.45.67/health
  API Docs: http://34.123.45.67/docs

🔧 Management commands:
  SSH: gcloud compute ssh buildbuzz-backend --zone=us-central1-a
  Logs: ./deployment/manage.sh logs
  Status: ./deployment/manage.sh status

✅ Application is healthy and running!

🚀 Deployment complete! Your BuildBuzz backend is now live!
```

## 🛠️ Configuration Options

### Environment Variables
```bash
# Deployment configuration
export GCP_PROJECT_ID="your-project-id"        # Required
export INSTANCE_NAME="buildbuzz-backend"       # Optional
export DB_INSTANCE_NAME="buildbuzz-db"         # Optional
export GCP_ZONE="us-central1-a"               # Optional
export GCP_REGION="us-central1"               # Optional
export MACHINE_TYPE="e2-medium"               # Optional
export DB_MACHINE_TYPE="db-f1-micro"          # Optional
```

### Custom Machine Types
```bash
# For development
export MACHINE_TYPE="e2-micro"
export DB_MACHINE_TYPE="db-f1-micro"

# For production
export MACHINE_TYPE="n1-standard-2"
export DB_MACHINE_TYPE="db-n1-standard-1"
```

## 🚨 Important Notes

1. **Billing**: Ensure billing is enabled for your GCP project
2. **Quotas**: Check that you have sufficient quotas for Compute Engine and Cloud SQL
3. **Permissions**: Your GCP account needs appropriate permissions (Editor or specific roles)
4. **Database Credentials**: Securely store the generated database credentials
5. **Firewall**: The script creates firewall rules allowing HTTP/HTTPS from anywhere

## 📈 Scaling and Updates

### Update Your Application
```bash
# Pull latest code and restart
./deployment/manage.sh update
```

### Scale Vertically
```bash
# Stop instance
gcloud compute instances stop buildbuzz-backend --zone=us-central1-a

# Change machine type
gcloud compute instances set-machine-type buildbuzz-backend \
  --machine-type=n1-standard-2 --zone=us-central1-a

# Start instance
gcloud compute instances start buildbuzz-backend --zone=us-central1-a
```

### Monitor Resources
```bash
# Check system status
./deployment/manage.sh status

# View logs
./deployment/manage.sh logs
```

## 🔒 Security Considerations

1. **Change default passwords** after deployment
2. **Restrict firewall rules** to specific IP ranges if needed
3. **Enable HTTPS** for production use
4. **Regular updates** of system packages and dependencies
5. **Backup strategy** for database and application data

## 🆘 Troubleshooting

### Common Issues

1. **Permission Denied**:
   ```bash
   # Make scripts executable
   chmod +x deployment/*.sh
   ```

2. **Project Not Found**:
   ```bash
   # Verify project exists and you have access
   gcloud projects list
   ```

3. **Quota Exceeded**:
   ```bash
   # Check quotas in GCP Console
   # Request quota increase if needed
   ```

4. **Application Not Starting**:
   ```bash
   # Check logs
   ./deployment/manage.sh logs
   
   # Check service status
   ./deployment/manage.sh status
   ```

### Getting Help
```bash
# View deployment script help
./deployment/deploy-one-command.sh --help

# View management script help
./deployment/manage.sh --help
```

---

## 🎯 Ready to Deploy?

1. **Install gcloud CLI** and authenticate
2. **Create or select** a GCP project
3. **Enable billing** for the project
4. **Run the deployment script**:
   ```bash
   chmod +x deployment/deploy-one-command.sh
   ./deployment/deploy-one-command.sh
   ```

That's it! Your BuildBuzz backend will be live on Google Cloud Platform in just a few minutes! 🚀