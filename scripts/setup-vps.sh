#!/bin/bash

# VPS Setup Script for KSO-AG-Ticketing
# Run this script on your VPS to prepare it for deployment

set -e

echo "🚀 Starting VPS Setup for KSO-AG-Ticketing..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="kso-ticketing"
APP_DIR="/opt/$APP_NAME"
STAGING_DIR="/opt/$APP_NAME-staging"
BACKUP_DIR="/opt/$APP_NAME/backups"
DOCKER_NETWORK="$APP_NAME-network"
STAGING_NETWORK="$APP_NAME-staging-network"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
   echo -e "${RED}Please run as root (use sudo)${NC}"
   exit 1
fi

echo -e "${GREEN}✓ Running with root privileges${NC}"

# Update system
echo -e "${YELLOW}📦 Updating system packages...${NC}"
apt update && apt upgrade -y

# Install required packages
echo -e "${YELLOW}📦 Installing required packages...${NC}"
apt install -y \
    docker.io \
    docker-compose \
    curl \
    wget \
    git \
    htop \
    ufw \
    nginx \
    certbot \
    python3-certbot-nginx \
    fail2ban

# Start and enable Docker
echo -e "${YELLOW}🐳 Starting Docker service...${NC}"
systemctl start docker
systemctl enable docker

# Add current user to docker group
if ! id -nG "$SUDO_USER" | grep -qw docker; then
    usermod -aG docker $SUDO_USER
    echo -e "${GREEN}✓ Added $SUDO_USER to docker group${NC}"
fi

# Create directories
echo -e "${YELLOW}📁 Creating application directories...${NC}"
mkdir -p $APP_DIR
mkdir -p $STAGING_DIR
mkdir -p $BACKUP_DIR
mkdir -p $APP_DIR/static
mkdir -p $APP_DIR/logs
mkdir -p $STAGING_DIR/static
mkdir -p $STAGING_DIR/logs

# Set permissions
chown -R $SUDO_USER:$SUDO_USER $APP_DIR
chown -R $SUDO_USER:$SUDO_USER $STAGING_DIR
chown -R $SUDO_USER:$SUDO_USER $BACKUP_DIR

# Create Docker networks
echo -e "${YELLOW}🌐 Creating Docker networks...${NC}"
docker network create $DOCKER_NETWORK || echo "Network already exists"
docker network create $STAGING_NETWORK || echo "Staging network already exists"

# Setup UFW firewall
echo -e "${YELLOW}🔒 Configuring firewall...${NC}"
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 9004/tcp  # Production app
ufw allow 9005/tcp  # Staging app
ufw --force enable

# Setup fail2ban
echo -e "${YELLOW}🛡️  Configuring fail2ban...${NC}"
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
EOF

systemctl restart fail2ban

# Create systemd service for monitoring
echo -e "${YELLOW}⚙️  Creating monitoring service...${NC}"
cat > /etc/systemd/system/kso-ticketing-monitor.service << EOF
[Unit]
Description=KSO Ticketing App Monitor
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
ExecStart=/usr/bin/docker ps --filter "name=kso-ticketing-app" --format "table {{.Names}}\t{{.Status}}"
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable kso-ticketing-monitor.service

# Create log rotation
echo -e "${YELLOW}📋 Setting up log rotation...${NC}"
cat > /etc/logrotate.d/kso-ticketing << EOF
$APP_DIR/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $SUDO_USER $SUDO_USER
    postrotate
        docker kill -s USR1 kso-ticketing-app || true
    endscript
}
EOF

# Create backup script
echo -e "${YELLOW}💾 Creating backup script...${NC}"
cat > /usr/local/bin/backup-kso-ticketing.sh << 'EOF'
#!/bin/bash

APP_NAME="kso-ticketing"
BACKUP_DIR="/opt/$APP_NAME/backups"
DATE=$(date +%Y%m%d_%H%M%S)
CONTAINER_NAME="$APP_NAME-app"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database if MySQL container exists
if docker ps | grep -q mysql; then
    echo "Creating database backup..."
    docker exec mysql mysqldump -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz
fi

# Backup container image
if docker ps | grep -q $CONTAINER_NAME; then
    echo "Creating container backup..."
    docker commit $CONTAINER_NAME $APP_NAME-backup:$DATE
    docker save $APP_NAME-backup:$DATE | gzip > $BACKUP_DIR/backup_$DATE.tar.gz
fi

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/backup_$DATE.tar.gz"
EOF

chmod +x /usr/local/bin/backup-kso-ticketing.sh

# Add to crontab for daily backups
echo -e "${YELLOW}⏰ Setting up daily backup...${NC}"
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-kso-ticketing.sh") | crontab -

# Create health check script
echo -e "${YELLOW}🏥 Creating health check script...${NC}"
cat > /usr/local/bin/health-check.sh << 'EOF'
#!/bin/bash

APP_NAME="kso-ticketing"
CONTAINER_NAME="$APP_NAME-app"
HEALTH_URL="http://localhost:9004/api/"

# Check if container is running
if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "Container $CONTAINER_NAME is not running!"
    exit 1
fi

# Check health endpoint
if curl -f -s $HEALTH_URL > /dev/null; then
    echo "✅ Application is healthy"
    exit 0
else
    echo "❌ Application health check failed"
    exit 1
fi
EOF

chmod +x /usr/local/bin/health-check.sh

# Setup SSL with Let's Encrypt (optional)
echo -e "${YELLOW}🔒 SSL Setup Instructions:${NC}"
echo "To setup SSL certificate, run:"
echo "certbot --nginx -d yourdomain.com"

# Display summary
echo -e "${GREEN}✅ VPS Setup Complete!${NC}"
echo ""
echo "📁 Application Directory: $APP_DIR"
echo "🌐 Production URL: http://$(curl -s ifconfig.me):9004"
echo "🧪 Staging URL: http://$(curl -s ifconfig.me):9005"
echo ""
echo "📋 Next Steps:"
echo "1. Push your code to GitLab"
echo "2. Configure GitLab CI/CD variables"
echo "3. Trigger deployment"
echo ""
echo "🔧 Useful Commands:"
echo "- View logs: docker logs -f kso-ticketing-app"
echo "- Check status: docker ps"
echo "- Health check: /usr/local/bin/health-check.sh"
echo "- Manual backup: /usr/local/bin/backup-kso-ticketing.sh"
echo ""
echo -e "${GREEN}🎉 Your VPS is ready for GitLab CI/CD deployment!${NC}"