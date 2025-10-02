# Deployment Script for Trouble Ticket System (PowerShell)
# Usage: .\scripts\deploy.ps1 [staging|production]

param(
    [Parameter(Position=0)]
    [ValidateSet("staging", "production")]
    [string]$Environment = "staging"
)

# Configuration
$BackupDir = "./backups"
$LogFile = "./logs/deploy.log"
$Date = Get-Date -Format "yyyyMMdd_HHmmss"

Write-Host "🚀 Starting deployment to $Environment environment..." -ForegroundColor Green

# Create necessary directories
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

# Function to log messages
function Log {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] $Message"
    Write-Host $LogEntry
    Add-Content -Path $LogFile -Value $LogEntry
}

# Function to backup current deployment
function Backup-Current {
    Log "📦 Creating backup of current deployment..."

    # Check if MySQL container is running
    $mysqlRunning = docker ps | Select-String "tickets_mysql" -Quiet
    if ($mysqlRunning) {
        $backupFile = "$BackupDir/backup_$Date.sql"
        $env:MYSQL_PWD = $env:MYSQL_ROOT_PASSWORD
        docker exec tickets_mysql mysqldump -u root tickets_db > $backupFile
        Log "✅ Database backup created: backup_$Date.sql"
    }

    # Backup application files
    $appBackup = "$BackupDir/app_backup_$Date.tar.gz"
    tar -czf $appBackup --exclude='.git' --exclude='node_modules' --exclude='__pycache__' --exclude='.env' .
    Log "✅ Application backup created: app_backup_$Date.tar.gz"
}

# Function to run tests
function Run-Tests {
    Log "🧪 Running tests..."

    try {
        # Backend tests
        Push-Location "backend"
        python -m pytest tests/ -v --cov=app --cov-report=term-missing
        if ($LASTEXITCODE -ne 0) {
            throw "Backend tests failed"
        }
        Pop-Location

        # Frontend tests
        Push-Location "frontend"
        npm run test:unit
        if ($LASTEXITCODE -ne 0) {
            throw "Frontend unit tests failed"
        }
        npm run build
        if ($LASTEXITCODE -ne 0) {
            throw "Frontend build failed"
        }
        Pop-Location

        Log "✅ All tests passed!"
    }
    catch {
        Log "❌ Tests failed: $_"
        throw
    }
}

# Function to deploy application
function Deploy-App {
    Log "🔧 Deploying application to $Environment..."

    try {
        if ($Environment -eq "production") {
            docker-compose -f docker-compose.prod.yml down
            docker-compose -f docker-compose.prod.yml pull
            docker-compose -f docker-compose.prod.yml up -d --build
        }
        else {
            docker-compose down
            docker-compose pull
            docker-compose up -d --build
        }

        if ($LASTEXITCODE -ne 0) {
            throw "Docker deployment failed"
        }

        Log "✅ Application deployed successfully!"
    }
    catch {
        Log "❌ Deployment failed: $_"
        throw
    }
}

# Function to health check
function Health-Check {
    Log "🏥 Running health checks..."

    # Wait for services to be ready
    Start-Sleep -Seconds 30

    # Check backend health
    $BackendUrl = "http://localhost:8000"
    try {
        $response = Invoke-WebRequest -Uri "$BackendUrl/health" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Log "✅ Backend health check passed"
        }
        else {
            throw "Backend health check failed with status code: $($response.StatusCode)"
        }
    }
    catch {
        Log "❌ Backend health check failed: $_"
        throw
    }

    # Check frontend health
    $FrontendUrl = "http://localhost"
    try {
        $response = Invoke-WebRequest -Uri "$FrontendUrl/health" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Log "✅ Frontend health check passed"
        }
        else {
            throw "Frontend health check failed with status code: $($response.StatusCode)"
        }
    }
    catch {
        Log "❌ Frontend health check failed: $_"
        throw
    }

    Log "✅ All health checks passed!"
}

# Function to notify success
function Notify-Success {
    Log "🎉 Deployment to $Environment completed successfully!"

    # Send notification (you can integrate with Slack, Teams, email, etc.)
    # Example: Send email or webhook notification here
}

# Main deployment process
function Main {
    Log "🎯 Starting deployment process for $Environment environment"

    # Load environment variables
    $envFile = ".env.$Environment"
    if (Test-Path $envFile) {
        Get-Content $envFile | Where-Object { $_ -notmatch '^#' -and $_.Trim() } | ForEach-Object {
            $key, $value = $_.Split('=', 2)
            [System.Environment]::SetEnvironmentVariable($key.Trim(), $value.Trim())
        }
        Log "✅ Loaded environment variables from $envFile"
    }
    elseif (Test-Path ".env") {
        Get-Content ".env" | Where-Object { $_ -notmatch '^#' -and $_.Trim() } | ForEach-Object {
            $key, $value = $_.Split('=', 2)
            [System.Environment]::SetEnvironmentVariable($key.Trim(), $value.Trim())
        }
        Log "⚠️  Environment file $envFile not found, using .env"
    }
    else {
        Log "⚠️  No environment file found, using existing environment variables"
    }

    try {
        # Run deployment steps
        Backup-Current
        Run-Tests
        Deploy-App
        Health-Check
        Notify-Success

        Log "🚀 Deployment completed successfully!"
    }
    catch {
        Log "❌ Deployment failed: $_"
        exit 1
    }
}

# Error handling
trap {
    Log "❌ Deployment failed! Check logs for details."
    exit 1
}

# Run main function
Main

Write-Host "✨ Deployment script completed. Check $LogFile for detailed logs." -ForegroundColor Cyan