#!/bin/bash

# Production Setup Script for Khel Bhoomi
echo "🚀 Setting up Khel Bhoomi for production deployment..."

# Function to generate JWT secret
generate_jwt_secret() {
    if command -v openssl > /dev/null; then
        openssl rand -base64 32
    else
        # Fallback to Python
        python3 -c "import secrets; print(secrets.token_urlsafe(32))"
    fi
}

# Create production environment files
echo "📁 Creating production environment files..."

# Backend production environment
cat > backend/.env.production << EOF
# Production Environment Variables for Backend
# Update these values for your deployment

# MongoDB Configuration (REQUIRED)
MONGO_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
DB_NAME=Khelbhoomi

# JWT Configuration (REQUIRED)
JWT_SECRET_KEY=$(generate_jwt_secret)

# CORS Configuration (Update with your frontend domain)
CORS_ORIGINS=https://your-frontend-service.onrender.com

# Server Configuration
HOST=0.0.0.0
PORT=10000
ENVIRONMENT=production

# Optional: API Configuration
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=60
MAX_FILE_SIZE=10485760
UPLOAD_FOLDER=uploads
LOG_LEVEL=INFO
EOF

# Frontend production environment
cat > frontend/.env.production << EOF
# Production Environment Variables for Frontend
# Update these values for your deployment

# Backend API URL (REQUIRED)
VITE_BACKEND_URL=https://your-backend-service.onrender.com

# Build Configuration
NODE_ENV=production

# Optional: WebSocket configuration
WDS_SOCKET_PORT=443

# Optional: Performance settings
VITE_LEGACY_SUPPORT=false
VITE_MINIFY=true
EOF

echo "✅ Production environment files created"
echo ""

# Check dependencies
echo "🔍 Checking dependencies..."

# Check if Python requirements are up to date
if [ -f "backend/requirements.txt" ]; then
    echo "✅ Backend requirements.txt found"
else
    echo "❌ Backend requirements.txt missing"
fi

# Check if frontend package.json exists
if [ -f "frontend/package.json" ]; then
    echo "✅ Frontend package.json found"
else
    echo "❌ Frontend package.json missing"
fi

echo ""
echo "🔧 Production setup recommendations:"
echo "1. Update MONGO_URL with your MongoDB Atlas connection string"
echo "2. Update VITE_BACKEND_URL with your backend service URL"
echo "3. Update CORS_ORIGINS with your frontend domain"
echo "4. Test locally before deploying to production"
echo ""

echo "📚 See RENDER_DEPLOYMENT_GUIDE.md for complete deployment instructions"
echo "✨ Production setup complete!"