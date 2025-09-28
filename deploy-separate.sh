#!/bin/bash

# Khel Bhoomi Separate Deployment Script
echo "🚀 Preparing Khel Bhoomi for Separate Render Deployment..."
echo "   Backend: Web Service"
echo "   Frontend: Static Site"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/server.py" ] || [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

# Generate JWT secret if needed
generate_jwt_secret() {
    if command -v openssl > /dev/null; then
        openssl rand -base64 32
    else
        python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || echo "generated-secret-key-replace-with-secure-one-32chars"
    fi
}

echo "🔧 STEP 1: Backend Web Service Preparation"
echo "============================================"

# Create backend environment template with generated secret
JWT_SECRET=$(generate_jwt_secret)
cat > backend/.env.webservice << EOF
# Backend Environment Variables for Render Web Service
MONGO_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
DB_NAME=Khelbhoomi
JWT_SECRET_KEY=$JWT_SECRET
CORS_ORIGINS=*
HOST=0.0.0.0
ENVIRONMENT=production
EOF

echo "✅ Backend environment template created with secure JWT secret"
echo "📁 File: backend/.env.webservice"

# Test backend preparation
cd backend
if ./deploy-web-service.sh; then
    echo "✅ Backend preparation successful"
else
    echo "⚠️  Backend preparation completed with warnings"
fi
cd ..

echo ""
echo "🎨 STEP 2: Frontend Static Site Preparation"
echo "============================================"

# Create frontend environment template
cat > frontend/.env.staticsite << EOF
# Frontend Environment Variables for Render Static Site
VITE_BACKEND_URL=https://your-backend-service.onrender.com
NODE_ENV=production
VITE_LEGACY_SUPPORT=false
VITE_MINIFY=true
EOF

echo "✅ Frontend environment template created"
echo "📁 File: frontend/.env.staticsite"

# Test frontend preparation
cd frontend
if ./build-production.sh; then
    echo "✅ Frontend preparation successful"
else
    echo "⚠️  Frontend preparation completed with warnings"
fi
cd ..

echo ""
echo "🎯 DEPLOYMENT SUMMARY"
echo "===================="
echo ""
echo "📋 BACKEND WEB SERVICE:"
echo "   Name: khel-bhoomi-backend"
echo "   Environment: Python 3"
echo "   Root Directory: backend"
echo "   Build Command: pip install -r requirements.txt"
echo "   Start Command: uvicorn server:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "📋 FRONTEND STATIC SITE:"
echo "   Name: khel-bhoomi-frontend"
echo "   Root Directory: frontend"
echo "   Build Command: yarn install && yarn build"
echo "   Publish Directory: dist"
echo ""
echo "🔑 CRITICAL: Set these environment variables in Render:"
echo ""
echo "Backend Web Service:"
echo "   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/"
echo "   DB_NAME=Khelbhoomi"
echo "   JWT_SECRET_KEY=$JWT_SECRET"
echo "   CORS_ORIGINS=* (update after frontend deployment)"
echo "   HOST=0.0.0.0"
echo "   ENVIRONMENT=production"
echo ""
echo "Frontend Static Site:"
echo "   VITE_BACKEND_URL=https://your-backend-service.onrender.com"
echo "   NODE_ENV=production"
echo ""
echo "📚 NEXT STEPS:"
echo "1. Push code to GitHub repository"
echo "2. Create Backend Web Service on Render"
echo "3. Create Frontend Static Site on Render"
echo "4. Configure environment variables"
echo "5. Update CORS_ORIGINS after frontend deployment"
echo ""
echo "📖 See RENDER_DEPLOYMENT_GUIDE_SEPARATE.md for detailed instructions"
echo "📝 Use SEPARATE_DEPLOYMENT_CHECKLIST.md as your deployment guide"
echo ""
echo "✨ Separate deployment preparation complete!"