# Deployment Guide

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Local Deployment](#local-deployment)
- [Production Deployment](#production-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring & Health Checks](#monitoring--health-checks)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### Required Software
- **Docker & Docker Compose** (latest versions)
- **Git** (for version control)
- **Node.js 18+** (for local development)
- **Python 3.11+** (for local development)

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: Minimum 20GB free space
- **Network**: Internet connection for package downloads

## 🌍 Environment Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd sistem-tiket-backend
```

### 2. Environment Files
Create environment files for different environments:

```bash
# Development
cp .env.example .env.development

# Staging
cp .env.example .env.staging

# Production
cp .env.example .env.production
```

### 3. Configure Environment Variables
Edit each environment file with appropriate settings:

**Critical Variables:**
```bash
# Database
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/tickets_db
MYSQL_ROOT_PASSWORD=strong_root_password_here
MYSQL_PASSWORD=strong_user_password_here

# Security
SECRET_KEY=your-super-secret-key-here-at-least-32-characters-long
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
MAX_LOGIN_ATTEMPTS=5
```

## 🏠 Local Deployment

### Quick Start
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Development Mode
```bash
# Start with rebuild
docker-compose up -d --build

# Access applications
# Frontend: http://localhost
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Database Management
```bash
# Access MySQL container
docker exec -it tickets_mysql mysql -u root -p

# Create database backup
docker exec tickets_mysql mysqldump -u root -p tickets_db > backup.sql

# Restore database
docker exec -i tickets_mysql mysql -u root -p tickets_db < backup.sql
```

## 🚀 Production Deployment

### Using Deployment Scripts

#### PowerShell (Windows)
```powershell
# Deploy to staging
.\scripts\deploy.ps1 staging

# Deploy to production
.\scripts\deploy.ps1 production
```

#### Bash (Linux/Mac)
```bash
# Make script executable
chmod +x scripts/deploy.sh

# Deploy to staging
./scripts/deploy.sh staging

# Deploy to production
./scripts/deploy.sh production
```

### Manual Production Deployment

#### 1. Prepare Production Environment
```bash
# Create secrets directory
mkdir -p secrets

# Create secret files
echo "your-strong-secret-key" > secrets/secret_key.txt
echo "your-mysql-password" > secrets/mysql_password.txt
echo "your-redis-password" > secrets/redis_password.txt
```

#### 2. Deploy with Docker Compose
```bash
# Deploy production stack
docker-compose -f docker-compose.prod.yml up -d --build

# Check service status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

#### 3. SSL Configuration
```bash
# Create SSL directory
mkdir -p ssl

# Add your SSL certificates
# ssl/cert.pem
# ssl/key.pem
```

## 🔄 CI/CD Pipeline

### GitHub Actions Setup

#### 1. Repository Settings
1. Go to repository **Settings > Environments**
2. Create environments: `staging`, `production`
3. Configure environment variables and secrets

#### 2. Required GitHub Secrets
```
# Repository Settings > Secrets and variables > Actions
MYSQL_ROOT_PASSWORD
MYSQL_PASSWORD
SECRET_KEY
REDIS_PASSWORD
```

#### 3. Environment Protection Rules
**Production Environment (Recommended):**
- ✅ Require reviewers (1-2 people)
- ✅ Wait timer (5 minutes)
- ✅ Restrict deployment to maintainers

### Pipeline Stages
1. **Security Scan** - Trivy vulnerability scanning
2. **Backend Tests** - pytest, Bandit, Safety checks
3. **Frontend Tests** - npm audit, build validation
4. **Code Quality** - ESLint, Prettier checks
5. **Deployment** - Automatic deploy to appropriate environment
6. **Health Check** - Post-deployment validation

### Manual Pipeline Triggers
```bash
# Trigger staging deployment
git push origin develop

# Trigger production deployment
git push origin main
```

## 📊 Monitoring & Health Checks

### Health Endpoints
- **Backend**: `GET /health`
- **Frontend**: `GET /health`

### Monitoring Stack (Production)
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001
  - Default credentials: admin/admin (change on first login)

### Log Management
```bash
# View application logs
docker-compose logs -f backend
docker-compose logs -f frontend

# View nginx logs
docker-compose logs -f nginx

# View database logs
docker-compose logs -f mysql
```

### Performance Monitoring
```bash
# Check resource usage
docker stats

# Check disk usage
docker system df

# Clean up unused resources
docker system prune -f
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```bash
# Check MySQL container
docker-compose ps mysql

# Check MySQL logs
docker-compose logs mysql

# Restart MySQL service
docker-compose restart mysql
```

#### 2. Frontend Build Failed
```bash
# Clear node_modules
docker-compose exec frontend rm -rf node_modules
docker-compose exec frontend npm install

# Rebuild frontend
docker-compose up -d --build frontend
```

#### 3. Backend API Not Responding
```bash
# Check backend container
docker-compose ps backend

# Check backend logs
docker-compose logs backend

# Restart backend service
docker-compose restart backend
```

#### 4. SSL Certificate Issues
```bash
# Check SSL certificates
ls -la ssl/

# Verify certificate syntax
openssl x509 -in ssl/cert.pem -text -noout

# Restart nginx after SSL changes
docker-compose restart nginx
```

### Performance Issues

#### High Memory Usage
```bash
# Check container resource usage
docker stats --no-stream

# Limit container memory (in docker-compose.yml)
services:
  backend:
    mem_limit: 1g
    memswap_limit: 1g
```

#### Slow Database Queries
```bash
# Enable slow query log
# Add to MySQL configuration:
# slow_query_log = 1
# long_query_time = 2

# Check active connections
docker exec tickets_mysql mysql -u root -p -e "SHOW PROCESSLIST;"
```

### Security Issues

#### Unauthorized Access
```bash
# Check authentication logs
docker-compose logs backend | grep -i auth

# Review failed login attempts
docker exec tickets_mysql mysql -u root -p -e "SELECT * FROM auth_logs WHERE success = 0 ORDER BY created_at DESC LIMIT 10;"
```

#### Vulnerability Scanning
```bash
# Run security scan locally
docker run --rm -v $(pwd):/app aquasec/trivy fs /app

# Check for secrets in code
git log --all --full-history -- **/secret*.key
```

## 📝 Maintenance

### Regular Tasks

#### Weekly
- [ ] Check and update dependencies
- [ ] Review security scan reports
- [ ] Backup database
- [ ] Clean up Docker resources

#### Monthly
- [ ] Update SSL certificates
- [ ] Review access logs
- [ ] Performance optimization
- [ ] Security audit

### Backup Procedures
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"

# Database backup
docker exec tickets_mysql mysqldump -u root -p$MYSQL_ROOT_PASSWORD tickets_db > $BACKUP_DIR/db_backup_$DATE.sql

# Application backup
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz --exclude='.git' --exclude='node_modules' .

# Clean old backups (keep last 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

## 🆘 Support

### Emergency Contacts
- **Development Team**: [team-email@company.com]
- **System Administrator**: [admin-email@company.com]

### Documentation
- **API Documentation**: http://localhost:8000/docs
- **System Architecture**: [link-to-architecture-docs]
- **Troubleshooting Guide**: [link-to-troubleshooting-docs]

### Change Management
All changes to production must follow the change management process:
1. Create feature branch from `develop`
2. Test in staging environment
3. Submit pull request to `main`
4. Review and approval
5. Deploy to production
6. Post-deployment verification

---

**Last Updated**: $(date +'%Y-%m-%d')
**Version**: 2.1.0
**Maintained by**: Development Team