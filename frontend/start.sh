#!/bin/bash

# Frontend startup script for Render
echo "🚀 Starting Khel Bhoomi Frontend..."

# Set default port if not provided
export PORT=${PORT:-3000}

# Load environment variables based on environment
if [ "$NODE_ENV" = "production" ]; then
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

# Check if build directory exists
if [ ! -d "dist" ]; then
    echo "📦 Building application..."
    yarn build
fi

echo "✅ Environment configured"
echo "🌍 Environment: ${NODE_ENV:-development}"
echo "🔗 Backend URL: ${VITE_BACKEND_URL}"
echo "🚪 Port: $PORT"
echo ""

# Start the server
if [ "$NODE_ENV" = "production" ]; then
    echo "🔥 Starting production server..."
    exec yarn preview --host 0.0.0.0 --port $PORT
else
    echo "🔥 Starting development server..."
    exec yarn dev --host 0.0.0.0 --port $PORT
fi