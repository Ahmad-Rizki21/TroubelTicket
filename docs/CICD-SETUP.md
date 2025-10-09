# GitLab CI/CD Setup Guide for KSO-AG-Ticketing

## 📋 Prerequisites

1. **GitLab Repository** dengan project ini
2. **VPS Server** (Ubuntu/Debian recommended) dengan:
   - Docker installed
   - SSH access
   - Domain (optional, untuk SSL)

## 🚀 Setup Instructions

### 1. Setup VPS Server

Copy file `scripts/setup-vps.sh` ke VPS dan jalankan:

```bash
# Di local machine
scp scripts/setup-vps.sh root@your-vps-ip:/tmp/

# Di VPS
chmod +x /tmp/setup-vps.sh
sudo /tmp/setup-vps.sh
```

### 2. GitLab CI/CD Variables

Buka GitLab → **Settings → CI/CD → Variables** dan tambahkan:

#### 📝 Required Variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `VPS_HOST` | `36.94.126.155` | IP VPS Anda |
| `VPS_USER` | `root` atau `ubuntu` | User VPS |
| `SSH_PRIVATE_KEY` | `[Private Key]` | SSH key untuk VPS |
| `CI_REGISTRY_PASSWORD` | `[GitLab Token]` | GitLab registry token |
| `CI_REGISTRY_USER` | `gitlab-ci-token` | GitLab registry user |

#### 🔐 Database Variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `mysql+pymysql://tickets_user:password@mysql:3306/tickets_db` | Database connection |
| `MYSQL_ROOT_PASSWORD` | `[strong password]` | MySQL root password |
| `MYSQL_DATABASE` | `tickets_db` | Database name |
| `MYSQL_USER` | `tickets_user` | Database user |
| `MYSQL_PASSWORD` | `[strong password]` | Database password |
| `SECRET_KEY` | `[32+ character key]` | JWT secret key |
| `CORS_ORIGINS` | `http://yourdomain.com,http://your-vps-ip:9004` | Allowed origins |

#### 🧪 Staging Variables (optional):

| Variable | Value | Description |
|----------|-------|-------------|
| `STAGING_DATABASE_URL` | `[staging DB connection]` | Staging database |
| `STAGING_SECRET_KEY` | `[staging secret key]` | Staging JWT secret |

### 3. SSH Key Setup

Generate SSH key di local:

```bash
ssh-keygen -t rsa -b 4096 -C "gitlab-ci-cd" -f ~/.ssh/gitlab_ci_rsa
```

Copy public key ke VPS:

```bash
ssh-copy-id -i ~/.ssh/gitlab_ci_rsa.pub root@your-vps-ip
```

Tambahkan private key ke GitLab CI/CD Variables:
- **Variable name:** `SSH_PRIVATE_KEY`
- **Value:** Content dari `~/.ssh/gitlab_ci_rsa`
- **Type:** File

### 4. GitLab Registry Setup

1. Buat GitLab Personal Access Token:
   - GitLab → **User Settings → Access Tokens**
   - Scopes: `read_registry`, `write_registry`
   - Copy token

2. Set CI/CD Variables:
   - `CI_REGISTRY_PASSWORD`: `[Personal Access Token]`
   - `CI_REGISTRY_USER`: `gitlab-ci-token`

### 5. Deployment Workflow

#### 🏗️ Production Deployment (branch `main`):
1. Push ke `main` branch
2. GitLab CI/CD akan:
   - Run tests
   - Build Docker image
   - Push ke GitLab Registry
   - Deploy ke VPS (manual trigger)
   - Health check

#### 🧪 Staging Deployment (branch `develop`):
1. Push ke `develop` branch
2. Auto-deploy ke staging (port 9005)

## 🐳 Docker Configuration

### Production Docker Compose (opsional):

```yaml
version: '3.8'

services:
  app:
    image: $CI_REGISTRY_IMAGE:latest
    container_name: kso-ticketing-app
    restart: unless-stopped
    ports:
      - "9004:8000"
    environment:
      - DATABASE_URL=$DATABASE_URL
      - SECRET_KEY=$SECRET_KEY
      - MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD
      - MYSQL_DATABASE=$MYSQL_DATABASE
      - MYSQL_USER=$MYSQL_USER
      - MYSQL_PASSWORD=$MYSQL_PASSWORD
      - CORS_ORIGINS=$CORS_ORIGINS
    volumes:
      - ./static:/app/static
      - ./logs:/app/logs
    networks:
      - kso-ticketing-network

  mysql:
    image: mysql:8.0
    container_name: kso-ticketing-mysql
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD
      - MYSQL_DATABASE=$MYSQL_DATABASE
      - MYSQL_USER=$MYSQL_USER
      - MYSQL_PASSWORD=$MYSQL_PASSWORD
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - kso-ticketing-network

volumes:
  mysql_data:

networks:
  kso-ticketing-network:
    driver: bridge
```

## 🔍 Monitoring & Maintenance

### Check Application Status:
```bash
# Di VPS
docker ps
docker logs -f kso-ticketing-app
/usr/local/bin/health-check.sh
```

### Backup Commands:
```bash
# Manual backup
/usr/local/bin/backup-kso-ticketing.sh

# List backups
ls -la /opt/kso-ticketing/backups/
```

### Rollback Commands:
```bash
# Load backup
docker load < /opt/kso-ticketing/backups/backup_[date].tar.gz
docker run -d --name kso-ticketing-rollback kso-ticketing-backup:[date]
```

## 🔧 Troubleshooting

### Common Issues:

1. **SSH Connection Failed:**
   - Cek SSH key: `ssh -T git@gitlab.com`
   - Verifikasi VPS SSH: `ssh root@your-vps-ip`

2. **Docker Build Failed:**
   - Cek Dockerfile di root directory
   - Verifikasi `.dockerignore`

3. **Database Connection Failed:**
   - Cek MySQL container: `docker ps | grep mysql`
   - Test connection: `docker exec -it mysql mysql -u root -p`

4. **Application Not Running:**
   - Cek logs: `docker logs kso-ticketing-app`
   - Cek port: `netstat -tlnp | grep 9004`

## 📊 Environment URLs

- **Production:** `http://your-vps-ip:9004`
- **Staging:** `http://your-vps-ip:9005`
- **GitLab Registry:** `registry.gitlab.com/username/project-name`

## 🎯 Best Practices

1. **Security:**
   - Gunakan strong passwords
   - Enable firewall
   - Regular backups
   - Monitor logs

2. **Performance:**
   - Optimize Docker image size
   - Use CDN untuk static files
   - Enable gzip compression

3. **Monitoring:**
   - Setup alerting
   - Monitor resource usage
   - Health checks

## 📞 Support

Jika ada masalah:
1. Cek GitLab CI/CD logs
2. Cek VPS logs: `journalctl -u docker`
3. Cek application logs: `docker logs kso-ticketing-app`
4. Review environment variables

---

🎉 **Your CI/CD pipeline is ready!** Push ke GitLab untuk auto-deployment.