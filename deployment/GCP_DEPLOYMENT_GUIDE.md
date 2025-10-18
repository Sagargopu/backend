# GCP Compute Engine Deployment Guide

## Overview
This guide will help you deploy the BuildBuzz FastAPI backend directly to Google Cloud Platform (GCP) Compute Engine without Docker.

## Prerequisites

1. **Google Cloud Account**: Active GCP account with billing enabled
2. **Google Cloud SDK**: Install `gcloud` CLI on your local machine
3. **Git Repository**: Your code should be pushed to GitHub
4. **Domain (Optional)**: For production SSL setup

## Deployment Architecture

```
Internet → Load Balancer (Optional) → Compute Engine VM
                                     ├── Nginx (Reverse Proxy)
                                     ├── Gunicorn (WSGI Server)
                                     └── FastAPI Application
                                     
Cloud SQL PostgreSQL ← Application
```

## Step-by-Step Deployment

### 1. Initial GCP Setup

```bash
# Install Google Cloud SDK (if not installed)
# Visit: https://cloud.google.com/sdk/docs/install

# Login to GCP
gcloud auth login

# Set your project (create one if needed)
gcloud config set project YOUR_PROJECT_ID

# Enable billing for your project (required)
# Visit: https://console.cloud.google.com/billing
```

### 2. Prepare Deployment Files

All deployment files are located in the `deployment/` directory:

- `startup.sh` - VM initialization script
- `deploy-gcp.sh` - Infrastructure deployment script
- `setup-cloudsql.sh` - Database setup script
- `update.sh` - Application update script
- `.env.production` - Production environment template

### 3. Configure Deployment Scripts

#### Update `deploy-gcp.sh`:
```bash
# Edit these variables in deploy-gcp.sh
PROJECT_ID="your-actual-project-id"
INSTANCE_NAME="buildbuzz-backend"
ZONE="us-central1-a"  # Choose your preferred zone
MACHINE_TYPE="e2-medium"  # Adjust based on your needs
```

#### Update `setup-cloudsql.sh`:
```bash
# Edit these variables in setup-cloudsql.sh
PROJECT_ID="your-actual-project-id"
INSTANCE_NAME="buildbuzz-db"
REGION="us-central1"  # Should match your compute zone region
```

### 4. Deploy Database (Cloud SQL)

```bash
# Make scripts executable
chmod +x deployment/*.sh

# Deploy Cloud SQL PostgreSQL
./deployment/setup-cloudsql.sh
```

**Important**: Save the database credentials from the output securely!

### 5. Configure Environment Variables

1. Copy the production environment template:
```bash
cp deployment/.env.production .env
```

2. Update `.env` with your actual values:
```bash
# Database URL from Cloud SQL setup
DATABASE_URL=postgresql://buildbuzz_user:PASSWORD@/buildbuzz?host=/cloudsql/PROJECT:REGION:INSTANCE

# Generate secure keys
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# Update other settings as needed
GOOGLE_CLOUD_PROJECT=your-project-id
CORS_ORIGINS=["https://yourdomain.com"]
```

### 6. Deploy Application

```bash
# Deploy Compute Engine instance and application
./deployment/deploy-gcp.sh
```

This script will:
- Create firewall rules
- Launch a Compute Engine instance
- Run the startup script automatically
- Install and configure the application

### 7. Verify Deployment

After deployment completes:

1. **Check Application Health**:
```bash
curl http://EXTERNAL_IP/health
```

2. **View Application Logs**:
```bash
gcloud compute ssh buildbuzz-backend --zone=us-central1-a \
  --command='sudo journalctl -u buildbuzz-backend -f'
```

3. **Test API Endpoints**:
```bash
curl http://EXTERNAL_IP/projects/
```

## Post-Deployment Configuration

### 1. SSL Certificate (Production)

For production, set up SSL with Let's Encrypt:

```bash
# SSH into your instance
gcloud compute ssh buildbuzz-backend --zone=us-central1-a

# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### 2. Domain Configuration

1. Point your domain to the instance's external IP
2. Update nginx configuration for your domain
3. Update CORS settings in `.env`

### 3. Monitoring Setup

```bash
# Install monitoring tools
sudo apt install htop nethogs

# Set up log rotation
sudo nano /etc/logrotate.d/buildbuzz
```

## Application Management

### Update Application

```bash
# SSH into instance
gcloud compute ssh buildbuzz-backend --zone=us-central1-a

# Run update script
sudo bash /opt/buildbuzz/backend/deployment/update.sh
```

### Restart Services

```bash
sudo systemctl restart buildbuzz-backend
sudo systemctl restart nginx
```

### View Logs

```bash
# Application logs
sudo journalctl -u buildbuzz-backend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Check Service Status

```bash
sudo systemctl status buildbuzz-backend
sudo systemctl status nginx
```

## Backup and Recovery

### Database Backup

```bash
# Automatic backups are enabled in Cloud SQL
# Manual backup:
gcloud sql backups create --instance=buildbuzz-db
```

### Application Backup

```bash
# Backup application files
sudo tar -czf /tmp/buildbuzz-backup-$(date +%Y%m%d).tar.gz /opt/buildbuzz/
```

## Scaling Considerations

### Vertical Scaling (Single Instance)

```bash
# Stop instance
gcloud compute instances stop buildbuzz-backend --zone=us-central1-a

# Change machine type
gcloud compute instances set-machine-type buildbuzz-backend \
  --machine-type=n1-standard-2 --zone=us-central1-a

# Start instance
gcloud compute instances start buildbuzz-backend --zone=us-central1-a
```

### Horizontal Scaling (Multiple Instances)

For high availability:
1. Create instance template
2. Set up managed instance group
3. Configure load balancer
4. Implement session management

## Troubleshooting

### Common Issues

1. **Application not starting**:
```bash
sudo journalctl -u buildbuzz-backend -f
sudo systemctl status buildbuzz-backend
```

2. **Database connection issues**:
```bash
# Test database connection
sudo -u buildbuzz /opt/buildbuzz/backend/venv/bin/python -c "
from app.database import engine
print(engine.execute('SELECT 1').scalar())
"
```

3. **Nginx issues**:
```bash
sudo nginx -t  # Test configuration
sudo systemctl status nginx
```

4. **Firewall issues**:
```bash
gcloud compute firewall-rules list
```

### Performance Monitoring

```bash
# System resources
htop
free -h
df -h

# Network connections
netstat -tlnp
```

## Security Best Practices

1. **Regular Updates**:
```bash
sudo apt update && sudo apt upgrade
```

2. **Firewall Configuration**:
```bash
# Only allow necessary ports
gcloud compute firewall-rules create allow-ssh \
  --allow tcp:22 --source-ranges YOUR_IP/32
```

3. **Database Security**:
- Use Cloud SQL with private IP
- Regular password rotation
- Enable audit logging

4. **Application Security**:
- Use environment variables for secrets
- Enable HTTPS only
- Implement rate limiting

## Cost Optimization

1. **Instance Sizing**: Start with `e2-micro` or `e2-small` for development
2. **Sustained Use Discounts**: Keep instances running for 25%+ of the month
3. **Committed Use Discounts**: For predictable workloads
4. **Preemptible Instances**: For development environments

## Maintenance Schedule

- **Weekly**: Check logs and system updates
- **Monthly**: Review performance metrics and costs
- **Quarterly**: Security updates and dependency updates
- **Yearly**: Review architecture and scaling needs

## Support

For issues:
1. Check application logs
2. Review GCP documentation
3. Check FastAPI documentation
4. Contact your development team

---

**Next Steps**: After successful deployment, configure monitoring, set up CI/CD pipeline, and plan for scaling.