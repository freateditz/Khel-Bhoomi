#!/bin/bash

# Khel Bhoomi Render Deployment Script
echo "🚀 Preparing Khel Bhoomi for Render deployment..."

# Create deployment checklist
echo "📋 Pre-deployment checklist:"
echo "✅ MongoDB Atlas cluster created and configured"
echo "✅ Environment variables prepared"
echo "✅ GitHub repository ready"
echo ""

# Check if MongoDB URL is set
if [ -z "$MONGO_URL" ]; then
    echo "⚠️  WARNING: MONGO_URL environment variable not set"
    echo "   Please set your MongoDB Atlas connection string"
fi

# Check if JWT secret is set
if [ -z "$JWT_SECRET_KEY" ]; then
    echo "⚠️  WARNING: JWT_SECRET_KEY environment variable not set"
    echo "   Please set a secure JWT secret key (32+ characters)"
fi

echo ""
echo "📁 Deployment files created:"
echo "   - render.yaml (Render Blueprint configuration)"
echo "   - .env.production (Production environment template)"
echo "   - RENDER_DEPLOYMENT_GUIDE.md (Complete deployment guide)"
echo "   - backend/.env.production (Backend environment template)"
echo "   - frontend/.env.production (Frontend environment template)"
echo ""

echo "🔧 Next steps:"
echo "1. Set up MongoDB Atlas database"
echo "2. Push code to GitHub repository"
echo "3. Create new Blueprint on Render using render.yaml"
echo "4. Configure environment variables in Render dashboard"
echo "5. Deploy and test!"
echo ""

echo "📚 For detailed instructions, see RENDER_DEPLOYMENT_GUIDE.md"
echo "✨ Deployment preparation complete!"