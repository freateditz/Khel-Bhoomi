#!/bin/bash

# Backend startup script for Render
echo "🚀 Starting Khel Bhoomi Backend..."

# Set default port if not provided
export PORT=${PORT:-8001}

# Load environment variables based on environment
if [ "$ENVIRONMENT" = "production" ]; then
    if [ -f ".env.production" ]; then
        echo "📄 Loading production environment..."
        export $(grep -v '^#' .env.production | xargs)
    fi
else
    if [ -f ".env" ]; then
        echo "📄 Loading development environment..."
        export $(grep -v '^#' .env | xargs)
    fi
fi

# Check required environment variables
if [ -z "$MONGO_URL" ]; then
    echo "❌ ERROR: MONGO_URL not set"
    exit 1
fi

if [ -z "$JWT_SECRET_KEY" ]; then
    echo "❌ ERROR: JWT_SECRET_KEY not set"
    exit 1
fi

echo "✅ Environment variables loaded"
echo "🌍 Environment: ${ENVIRONMENT:-development}"
echo "🔗 MongoDB: ${MONGO_URL:0:20}..."
echo "🔑 JWT Secret: ${JWT_SECRET_KEY:0:10}..."
echo "🚪 Port: $PORT"
echo ""

# Start the server
echo "🔥 Starting FastAPI server..."
exec uvicorn server:app --host 0.0.0.0 --port $PORT