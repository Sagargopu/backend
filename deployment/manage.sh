#!/bin/bash

# GCP Management Script for BuildBuzz Backend
# Manage your deployed application from the command line

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-}"
INSTANCE_NAME="${INSTANCE_NAME:-buildbuzz-backend}"
ZONE="${GCP_ZONE:-us-central1-a}"

print_usage() {
    echo -e "${BLUE}BuildBuzz Backend - GCP Management Script${NC}"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  status      - Check application and services status"
    echo "  logs        - View application logs (follow mode)"
    echo "  restart     - Restart the application service"
    echo "  update      - Pull latest code and restart"
    echo "  ssh         - SSH into the instance"
    echo "  ip          - Get instance external IP"
    echo "  health      - Check application health"
    echo "  stop        - Stop the application"
    echo "  start       - Start the application"
    echo "  backup      - Create application backup"
    echo "  env         - Edit environment variables"
    echo ""
    echo "Options:"
    echo "  --project   - GCP Project ID"
    echo "  --instance  - Instance name (default: buildbuzz-backend)"
    echo "  --zone      - GCP Zone (default: us-central1-a)"
    echo ""
    echo "Examples:"
    echo "  $0 status"
    echo "  $0 logs"
    echo "  $0 update --project my-project"
    echo "  $0 ssh"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            PROJECT_ID="$2"
            shift 2
            ;;
        --instance)
            INSTANCE_NAME="$2"
            shift 2
            ;;
        --zone)
            ZONE="$2"
            shift 2
            ;;
        status|logs|restart|update|ssh|ip|health|stop|start|backup|env)
            COMMAND="$1"
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Check if command is provided
if [ -z "$COMMAND" ]; then
    print_usage
    exit 1
fi

# Prompt for project if not set
if [ -z "$PROJECT_ID" ]; then
    echo -n "Enter your GCP Project ID: "
    read PROJECT_ID
fi

# Set project
gcloud config set project $PROJECT_ID

# Execute commands
case $COMMAND in
    status)
        echo -e "${BLUE}📊 Checking application status...${NC}"
        gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='
            echo "=== System Status ==="
            uptime
            echo ""
            echo "=== Application Service ==="
            sudo systemctl status buildbuzz-backend --no-pager
            echo ""
            echo "=== Nginx Service ==="
            sudo systemctl status nginx --no-pager
            echo ""
            echo "=== Disk Usage ==="
            df -h
            echo ""
            echo "=== Memory Usage ==="
            free -h
        '
        ;;
    
    logs)
        echo -e "${BLUE}📋 Following application logs (Ctrl+C to exit)...${NC}"
        gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo journalctl -u buildbuzz-backend -f'
        ;;
    
    restart)
        echo -e "${YELLOW}🔄 Restarting application...${NC}"
        gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='
            sudo systemctl restart buildbuzz-backend
            sudo systemctl status buildbuzz-backend --no-pager
        '
        echo -e "${GREEN}✅ Application restarted${NC}"
        ;;
    
    update)
        echo -e "${BLUE}🔄 Updating application...${NC}"
        gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='
            sudo systemctl stop buildbuzz-backend
            sudo -u buildbuzz bash << "EOF"
cd /opt/buildbuzz/backend
git pull origin sagar-test-users
source venv/bin/activate
pip install -r requirements.txt
EOF
            sudo systemctl start buildbuzz-backend
            sudo systemctl status buildbuzz-backend --no-pager
        '
        echo -e "${GREEN}✅ Application updated${NC}"
        ;;
    
    ssh)
        echo -e "${BLUE}🔐 Connecting to instance...${NC}"
        gcloud compute ssh $INSTANCE_NAME --zone=$ZONE
        ;;
    
    ip)
        EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
        echo -e "${GREEN}🌐 External IP: $EXTERNAL_IP${NC}"
        echo "   Main URL: http://$EXTERNAL_IP"
        echo "   Health: http://$EXTERNAL_IP/health"
        echo "   Docs: http://$EXTERNAL_IP/docs"
        ;;
    
    health)
        EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
        echo -e "${BLUE}🏥 Checking application health...${NC}"
        
        if curl -f -s http://$EXTERNAL_IP/health; then
            echo -e "${GREEN}✅ Application is healthy!${NC}"
        else
            echo -e "${RED}❌ Application health check failed${NC}"
            echo "Checking service status..."
            gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo systemctl status buildbuzz-backend --no-pager'
        fi
        ;;
    
    stop)
        echo -e "${YELLOW}⏹️  Stopping application...${NC}"
        gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='sudo systemctl stop buildbuzz-backend'
        echo -e "${GREEN}✅ Application stopped${NC}"
        ;;
    
    start)
        echo -e "${GREEN}▶️  Starting application...${NC}"
        gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='
            sudo systemctl start buildbuzz-backend
            sudo systemctl status buildbuzz-backend --no-pager
        '
        echo -e "${GREEN}✅ Application started${NC}"
        ;;
    
    backup)
        BACKUP_NAME="buildbuzz-backup-$(date +%Y%m%d-%H%M%S)"
        echo -e "${BLUE}💾 Creating backup: $BACKUP_NAME${NC}"
        gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="
            sudo tar -czf /tmp/$BACKUP_NAME.tar.gz /opt/buildbuzz/backend
            echo 'Backup created: /tmp/$BACKUP_NAME.tar.gz'
        "
        echo -e "${GREEN}✅ Backup created on instance${NC}"
        echo "To download: gcloud compute scp $INSTANCE_NAME:/tmp/$BACKUP_NAME.tar.gz ./ --zone=$ZONE"
        ;;
    
    env)
        echo -e "${BLUE}⚙️  Opening environment file for editing...${NC}"
        gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='
            sudo cp /opt/buildbuzz/backend/.env /tmp/.env.backup
            sudo nano /opt/buildbuzz/backend/.env
            echo "Environment file updated. Restart application to apply changes."
            echo "To restart: sudo systemctl restart buildbuzz-backend"
        '
        ;;
    
    *)
        echo -e "${RED}❌ Unknown command: $COMMAND${NC}"
        print_usage
        exit 1
        ;;
esac