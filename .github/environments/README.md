# GitHub Environments Configuration

Untuk menggunakan deployment environments dengan aman, Anda perlu setup environments di GitHub repository settings.

## Setup Steps:

### 1. Repository Settings
- Go to repository Settings > Environments
- Create two environments: `staging` dan `production`

### 2. Environment Variables

#### Staging Environment
```
ENVIRONMENT=staging
DATABASE_URL=staging-database-url
SECRET_KEY=staging-secret-key
CORS_ORIGINS=["http://staging.yourdomain.com"]
```

#### Production Environment
```
ENVIRONMENT=production
DATABASE_URL=production-database-url
SECRET_KEY=production-secret-key
CORS_ORIGINS=["https://yourdomain.com"]
```

### 3. Protection Rules (Optional but Recommended)

#### Production Environment:
- Require reviewers (1-2 people)
- Wait timer (5 minutes)
- Restrict who can deploy (only maintainers)

#### Staging Environment:
- No restrictions for faster deployment

### 4. Updated CI/CD with Environment Support

Jika Anda ingin menggunakan environments setelah setup, update workflow menjadi:

```yaml
deploy-staging:
  needs: [security-scan, backend-tests, frontend-tests, code-quality, security-headers]
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/develop'
  environment: staging

  steps:
  - uses: actions/checkout@v4

  - name: Deploy to staging
    run: |
      echo "Deploy to staging environment"
      # Deploy commands here

deploy-production:
  needs: [security-scan, backend-tests, frontend-tests, code-quality, security-headers]
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main'
  environment: production

  steps:
  - uses: actions/checkout@v4

  - name: Deploy to production
    run: |
      echo "Deploy to production environment"
      # Deploy commands here
```

## Benefits of Using Environments:

1. **Security**: Environment-specific secrets and variables
2. **Control**: Deployment protection rules
3. **Tracking**: Better deployment history and visibility
4. **Isolation**: Separate configurations for different environments

## Security Best Practices:

- Use different secrets for each environment
- Implement protection rules for production
- Use environment-specific database credentials
- Monitor deployments with audit logs