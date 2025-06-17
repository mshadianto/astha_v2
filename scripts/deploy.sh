# ===== scripts/deploy.sh =====
#!/bin/bash

# ASTHA Deployment Script
# Usage: ./deploy.sh [environment]

set -e

ENVIRONMENT=${1:-development}
PROJECT_NAME="astha-hajj-analytics"

echo "🚀 Deploying ASTHA to $ENVIRONMENT environment..."

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(development|staging|production)$ ]]; then
    echo "❌ Invalid environment. Use: development, staging, or production"
    exit 1
fi

# Load environment-specific variables
case $ENVIRONMENT in
    development)
        DOCKER_COMPOSE_FILE="docker-compose.yml"
        ;;
    staging)
        DOCKER_COMPOSE_FILE="docker-compose.staging.yml"
        ;;
    production)
        DOCKER_COMPOSE_FILE="docker-compose.prod.yml"
        ;;
esac

echo "📁 Using compose file: $DOCKER_COMPOSE_FILE"

# Pre-deployment checks
echo "🔍 Running pre-deployment checks..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi

# Check if required files exist
if [[ ! -f ".env" ]]; then
    echo "❌ .env file not found"
    exit 1
fi

if [[ ! -f "$DOCKER_COMPOSE_FILE" ]]; then
    echo "❌ Docker compose file not found: $DOCKER_COMPOSE_FILE"
    exit 1
fi

# Backup existing data (production only)
if [[ "$ENVIRONMENT" == "production" ]]; then
    echo "💾 Creating backup..."
    python scripts/backup.py --cleanup-only
    python scripts/backup.py
fi

# Pull latest images
echo "📥 Pulling latest images..."
docker-compose -f $DOCKER_COMPOSE_FILE pull

# Build application image
echo "🔨 Building application..."
docker-compose -f $DOCKER_COMPOSE_FILE build

# Stop existing services
echo "⏹️ Stopping existing services..."
docker-compose -f $DOCKER_COMPOSE_FILE down

# Start services
echo "▶️ Starting services..."
docker-compose -f $DOCKER_COMPOSE_FILE up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Health check
echo "🏥 Running health checks..."
max_retries=30
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
        echo "✅ Application is healthy"
        break
    fi
    
    retry_count=$((retry_count + 1))
    echo "⏳ Health check attempt $retry_count/$max_retries..."
    sleep 10
done

if [ $retry_count -eq $max_retries ]; then
    echo "❌ Health check failed after $max_retries attempts"
    echo "📋 Service logs:"
    docker-compose -f $DOCKER_COMPOSE_FILE logs --tail=50
    exit 1
fi

# Show service status
echo "📊 Service status:"
docker-compose -f $DOCKER_COMPOSE_FILE ps

# Clean up old images
echo "🧹 Cleaning up old images..."
docker image prune -f

echo "🎉 Deployment completed successfully!"
echo "🌐 Application URL: http://localhost:8501"

if [[ "$ENVIRONMENT" == "production" ]]; then
    echo "📧 Sending deployment notification..."
    # Add notification logic here (email, Slack, etc.)
fi
