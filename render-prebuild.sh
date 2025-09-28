#!/bin/bash

# Render pre-build script
echo "🔧 Running Khel Bhoomi pre-build setup..."

# Make scripts executable
chmod +x backend/start.sh
chmod +x frontend/start.sh
chmod +x deploy.sh
chmod +x setup-production.sh

# Check if we're building backend or frontend
if [ -f "backend/requirements.txt" ]; then
    echo "🐍 Backend environment detected"
    cd backend
    
    # Check Python version
    python3 --version
    
    # Install dependencies
    echo "📦 Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo "✅ Backend dependencies installed"
elif [ -f "frontend/package.json" ]; then
    echo "⚛️  Frontend environment detected"
    cd frontend
    
    # Check Node version
    node --version
    yarn --version
    
    # Install dependencies
    echo "📦 Installing Node dependencies..."
    yarn install --frozen-lockfile
    
    echo "✅ Frontend dependencies installed"
fi

echo "🎉 Pre-build setup complete!"