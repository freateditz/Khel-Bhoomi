#!/bin/bash

# Render Backend Deployment Script for Khel Bhoomi

echo "🚀 Starting Khel Bhoomi Backend Deployment..."

# Install dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip install -r requirements.txt

echo "✅ Backend deployment ready!"
echo "🌟 Use start command: uvicorn server:app --host 0.0.0.0 --port $PORT"