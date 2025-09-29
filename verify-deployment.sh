#!/bin/bash

echo "🔍 Verifying Khel Bhoomi Deployment Readiness..."

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found!"
    exit 1
fi

# Check key configuration files
echo "📋 Checking configuration files..."

files=(
    "frontend/package.json"
    "frontend/postcss.config.js" 
    "frontend/tailwind.config.js"
    "frontend/vite.config.js"
    "frontend/_redirects"
    "frontend/render-build.sh"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file - Found"
    else
        echo "❌ $file - Missing"
        exit 1
    fi
done

# Test build process
echo ""
echo "🔨 Testing build process..."
cd frontend

# Clean previous build
if [ -d "dist" ]; then
    rm -rf dist
    echo "🗑️ Cleaned previous build"
fi

# Install dependencies
echo "📦 Installing dependencies..."
yarn install --silent > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Run build
echo "⚙️ Running build..."
yarn build:static > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully"
else
    echo "❌ Build failed"
    exit 1
fi

# Check if required files exist in dist
dist_files=(
    "dist/index.html"
    "dist/_redirects"
    "dist/assets"
)

for file in "${dist_files[@]}"; do
    if [ -e "$file" ]; then
        echo "✅ $file - Generated"
    else
        echo "❌ $file - Missing"
        exit 1
    fi
done

# Get build size info
if [ -f "dist/index.html" ]; then
    size=$(du -sh dist | cut -f1)
    echo "📊 Build size: $size"
fi

echo ""
echo "🎉 Deployment Verification Complete!"
echo ""
echo "✅ All checks passed - Your frontend is ready for Render deployment!"
echo ""
echo "📋 Next Steps:"
echo "1. Push your code to GitHub"
echo "2. Create a Static Site on Render"
echo "3. Use build command: yarn build:static"
echo "4. Set publish directory: dist"
echo "5. Set root directory: frontend"
echo ""
echo "🌐 Don't forget to set VITE_BACKEND_URL environment variable!"