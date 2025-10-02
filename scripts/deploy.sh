#!/bin/bash

# Deployment Script for Trouble Ticket System
# Usage: ./scripts/deploy.sh [staging|production]

set -e

# Configuration
ENVIRONMENT=${1:-staging}
BACKUP_DIR="./backups"
LOG_FILE="./logs/deploy.log"
DATE=$(date +%Y%m%d_%H%M%S)

echo "🚀 Starting deployment to $ENVIRONMENT environment..."

# Create necessary directories
mkdir -p $BACKUP_DIR
mkdir -p logs

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# Function to backup current deployment
backup_current() {
    log "📦 Creating backup of current deployment..."

    if docker ps | grep -q tickets_backend; then
        docker exec tickets_backend_prod mysqldump -u root -p$MYSQL_ROOT_PASSWORD tickets_db > $BACKUP_DIR/backup_$DATE.sql
        log "✅ Database backup created: backup_$DATE.sql"
    fi

    # Backup application files
    tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz --exclude='.git' --exclude='node_modules' --exclude='__pycache__' --exclude='.env' .
    log "✅ Application backup created: app_backup_$DATE.tar.gz"
}

# Function to run tests
run_tests() {
    log "🧪 Running tests..."

    # Backend tests
    cd backend
    python -m pytest tests/ -v --cov=app --cov-report=term-missing
    cd ..

    # Frontend tests
    cd frontend
    npm run test:unit
    npm run build
    cd ..

    log "✅ All tests passed!"
}

# Function to deploy application
deploy_app() {
    log "🔧 Deploying application to $ENVIRONMENT..."

    if [ "$ENVIRONMENT" = "production" ]; then
        docker-compose -f docker-compose.prod.yml down
        docker-compose -f docker-compose.prod.yml pull
        docker-compose -f docker-compose.prod.yml up -d --build
    else
        docker-compose down
        docker-compose pull
        docker-compose up -d --build
    fi

    log "✅ Application deployed successfully!"
}

# Function to health check
health_check() {
    log "🏥 Running health checks..."

    # Wait for services to be ready
    sleep 30

    # Check backend health
    BACKEND_URL="http://localhost:8000"
    if curl -f $BACKEND_URL/health > /dev/null 2>&1; then
        log "✅ Backend health check passed"
    else
        log "❌ Backend health check failed"
        exit 1
    fi

    # Check frontend health
    FRONTEND_URL="http://localhost"
    if curl -f $FRONTEND_URL/health > /dev/null 2>&1; then
        log "✅ Frontend health check passed"
    else
        log "❌ Frontend health check failed"
        exit 1
    fi

    log "✅ All health checks passed!"
}

# Function to notify
notify_success() {
    log "🎉 Deployment to $ENVIRONMENT completed successfully!"

    # Send notification (you can integrate with Slack, email, etc.)
    # Example: curl -X POST -H 'Content-type: application/json' \
    #   --data '{"text":"✅ Trouble Ticket System deployed to '$ENVIRONMENT' successfully!"}' \
    #   YOUR_SLACK_WEBHOOK_URL
}

# Main deployment process
main() {
    log "🎯 Starting deployment process for $ENVIRONMENT environment"

    # Load environment variables
    if [ -f .env.$ENVIRONMENT ]; then
        export $(cat .env.$ENVIRONMENT | grep -v '^#' | xargs)
    else
        log "⚠️  Environment file .env.$ENVIRONMENT not found, using .env"
        export $(cat .env | grep -v '^#' | xargs)
    fi

    # Run deployment steps
    backup_current
    run_tests
    deploy_app
    health_check
    notify_success

    log "🚀 Deployment completed successfully!"
}

# Error handling
trap 'log "❌ Deployment failed! Check logs for details."; exit 1' ERR

# Run main function
main

echo "✨ Deployment script completed. Check $LOG_FILE for detailed logs."