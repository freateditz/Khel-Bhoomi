#!/bin/bash

# Frontend Production Build Script for Render Static Site
echo "🏗️  Building Khel Bhoomi Frontend for Production..."

# Load environment variables
if [ -f ".env.production" ]; then
    echo "📄 Loading production environment..."
    export $(grep -v '^#' .env.production | xargs)
elif [ -f ".env" ]; then
    echo "📄 Loading environment file..."
    export $(grep -v '^#' .env | xargs)
fi

# Verify required environment variables
if [ -z "$VITE_BACKEND_URL" ]; then
    echo "⚠️  WARNING: VITE_BACKEND_URL not set"
    echo "   Set it to your backend service URL: https://your-backend.onrender.com"
fi

echo "✅ Environment configured"
echo "🔗 Backend URL: ${VITE_BACKEND_URL}"
echo "🌍 Node Environment: ${NODE_ENV:-development}"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
yarn install --frozen-lockfile

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Build the application
echo "🔨 Building React application..."
yarn build

if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully"
    echo "📂 Build output in 'dist' directory"
    
    # Show build stats
    if [ -d "dist" ]; then
        echo "📊 Build statistics:"
        du -sh dist/
        find dist -name "*.js" -o -name "*.css" | wc -l | xargs echo "   Files:"
    fi
else
    echo "❌ Build failed"
    exit 1
fi

echo ""
echo "🎉 Frontend build ready for Render Static Site deployment!"
echo "📋 Next steps:"
echo "   1. Push code to GitHub"
echo "   2. Create Render Static Site"
echo "   3. Set Root Directory: frontend"
echo "   4. Set Publish Directory: dist"
echo "   5. Deploy!"