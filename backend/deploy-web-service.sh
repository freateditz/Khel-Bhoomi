#!/bin/bash

# Backend Web Service Deployment Script for Render
echo "🚀 Preparing Khel Bhoomi Backend for Render Web Service..."

# Load environment variables
if [ -f ".env.production" ]; then
    echo "📄 Loading production environment..."
    export $(grep -v '^#' .env.production | xargs)
elif [ -f ".env" ]; then
    echo "📄 Loading environment file..."
    export $(grep -v '^#' .env | xargs)
fi

# Verify required environment variables
required_vars=("MONGO_URL" "JWT_SECRET_KEY" "DB_NAME")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -gt 0 ]; then
    echo "⚠️  WARNING: Missing required environment variables:"
    for var in "${missing_vars[@]}"; do
        echo "   - $var"
    done
    echo ""
    echo "💡 Set these in your Render Web Service environment variables"
fi

echo "✅ Environment check completed"
echo "🔗 MongoDB: ${MONGO_URL:0:25}..."
echo "🔑 JWT Secret: ${JWT_SECRET_KEY:0:8}..."
echo "💾 Database: ${DB_NAME}"
echo "🌍 Environment: ${ENVIRONMENT:-production}"
echo ""

# Check Python dependencies
echo "🔍 Checking Python dependencies..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
    echo "📦 Dependencies to install:"
    cat requirements.txt | sed 's/^/   - /'
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Test local installation (optional)
if command -v pip > /dev/null; then
    echo ""
    echo "🧪 Testing local installation..."
    pip install -r requirements.txt --quiet
    
    if [ $? -eq 0 ]; then
        echo "✅ All dependencies can be installed successfully"
    else
        echo "❌ Some dependencies failed to install"
        echo "   Check requirements.txt for compatibility issues"
    fi
fi

echo ""
echo "🎯 Render Web Service Configuration:"
echo "   Name: khel-bhoomi-backend"
echo "   Environment: Python 3"
echo "   Root Directory: backend"
echo "   Build Command: pip install -r requirements.txt"
echo "   Start Command: uvicorn server:app --host 0.0.0.0 --port \$PORT"
echo ""

echo "🔑 Required Environment Variables for Render:"
echo "   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/"
echo "   DB_NAME=Khelbhoomi"
echo "   JWT_SECRET_KEY=your-secure-32-character-secret"
echo "   CORS_ORIGINS=https://your-frontend-site.onrender.com"
echo "   HOST=0.0.0.0"
echo "   ENVIRONMENT=production"
echo ""

echo "🎉 Backend ready for Render Web Service deployment!"
echo "📋 Next steps:"
echo "   1. Push code to GitHub"
echo "   2. Create Render Web Service"
echo "   3. Set Root Directory: backend"
echo "   4. Add environment variables"
echo "   5. Deploy!"