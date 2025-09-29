#!/bin/bash

# Render Static Site Build Script for Khel Bhoomi Frontend
# This script is optimized for Render's static site deployment

echo "🚀 Starting Khel Bhoomi Frontend Build for Render..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
yarn install --frozen-lockfile

# Build for production
echo "🔨 Building for production..."
yarn build:static

# Copy _redirects file to dist for SPA routing
echo "📋 Setting up SPA routing..."
cp _redirects dist/

echo "✅ Build completed successfully!"
echo "📁 Built files are in: frontend/dist/"
echo "🌟 Your Khel Bhoomi app is ready for deployment!"