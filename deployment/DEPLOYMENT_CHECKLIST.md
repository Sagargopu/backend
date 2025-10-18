# GCP Deployment Checklist

## Pre-Deployment
- [ ] GCP account with billing enabled
- [ ] Google Cloud SDK installed and authenticated
- [ ] Project created in GCP Console
- [ ] Code pushed to GitHub repository
- [ ] Domain name configured (if using custom domain)

## Configuration
- [ ] Updated `PROJECT_ID` in deployment scripts
- [ ] Configured `ZONE` and `REGION` preferences
- [ ] Chosen appropriate `MACHINE_TYPE` for your needs
- [ ] Reviewed firewall rules requirements

## Database Setup
- [ ] Run `./deployment/setup-cloudsql.sh`
- [ ] Save database credentials securely
- [ ] Test database connectivity
- [ ] Configure database backup schedule

## Environment Configuration
- [ ] Copy `.env.production` to `.env`
- [ ] Update `DATABASE_URL` with Cloud SQL credentials
- [ ] Generate and set `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Configure `CORS_ORIGINS` for your frontend domain
- [ ] Set `GOOGLE_CLOUD_PROJECT` ID
- [ ] Review and update other environment variables

## Application Deployment
- [ ] Make deployment scripts executable (`chmod +x deployment/*.sh`)
- [ ] Run `./deployment/deploy-gcp.sh`
- [ ] Wait for deployment to complete (5-10 minutes)
- [ ] Note the external IP address from output

## Post-Deployment Verification
- [ ] Test health endpoint: `curl http://EXTERNAL_IP/health`
- [ ] Test API endpoints: `curl http://EXTERNAL_IP/projects/`
- [ ] Check application logs for errors
- [ ] Verify database connection is working
- [ ] Test all major API functionalities

## Production Configuration (Optional)
- [ ] Configure custom domain DNS
- [ ] Set up SSL certificate with Let's Encrypt
- [ ] Update nginx configuration for domain
- [ ] Configure monitoring and alerting
- [ ] Set up log aggregation
- [ ] Configure automatic backups

## Security Hardening
- [ ] Change default passwords
- [ ] Configure SSH key-based authentication
- [ ] Set up firewall rules for specific IP ranges
- [ ] Enable Cloud SQL private IP (if needed)
- [ ] Review and limit service account permissions
- [ ] Enable audit logging

## Monitoring Setup
- [ ] Configure uptime monitoring
- [ ] Set up resource usage alerts
- [ ] Configure log-based metrics
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Configure performance monitoring

## Documentation
- [ ] Document deployment process
- [ ] Share credentials with team (securely)
- [ ] Create incident response procedures
- [ ] Document backup and recovery procedures

## Testing
- [ ] Run full API test suite
- [ ] Test database operations
- [ ] Verify file uploads work
- [ ] Test authentication flows
- [ ] Check CORS configuration
- [ ] Validate environment-specific configurations

## Maintenance Setup
- [ ] Schedule regular system updates
- [ ] Configure automated database backups
- [ ] Set up monitoring dashboards
- [ ] Plan capacity scaling procedures
- [ ] Document troubleshooting steps

---

## Quick Commands Reference

### Check Application Status
```bash
gcloud compute ssh buildbuzz-backend --zone=us-central1-a --command='sudo systemctl status buildbuzz-backend'
```

### View Application Logs
```bash
gcloud compute ssh buildbuzz-backend --zone=us-central1-a --command='sudo journalctl -u buildbuzz-backend -f'
```

### Update Application
```bash
gcloud compute ssh buildbuzz-backend --zone=us-central1-a --command='sudo bash /opt/buildbuzz/backend/deployment/update.sh'
```

### Restart Services
```bash
gcloud compute ssh buildbuzz-backend --zone=us-central1-a --command='sudo systemctl restart buildbuzz-backend nginx'
```