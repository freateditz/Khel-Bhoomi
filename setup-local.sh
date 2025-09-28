#!/bin/bash

echo "🚀 Starting Khel Bhoomi Local Development Environment"
echo "=================================================="

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo "🔍 Checking dependencies..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

if ! command_exists yarn; then
    echo "❌ Yarn is not installed. Please install Yarn package manager."
    exit 1
fi

echo "✅ All dependencies found!"

# Setup backend
echo "🔧 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating backend .env file from template..."
    cp .env.example .env
    echo "⚠️ Please edit backend/.env with your MongoDB connection and other settings"
fi

cd ..

# Setup frontend
echo "🔧 Setting up frontend..."
cd frontend

# Install Node dependencies
echo "📦 Installing Node.js dependencies..."
yarn install

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating frontend .env file from template..."
    cp .env.example .env
    echo "⚠️ Please edit frontend/.env with your backend URL"
fi

cd ..

echo "✅ Setup complete!"
echo ""
echo "🚀 To start development:"
echo "1. Start backend: cd backend && source venv/bin/activate && python main.py"
echo "2. Start frontend: cd frontend && yarn dev"
echo ""
echo "🌐 URLs:"
echo "- Backend: http://localhost:8001"
echo "- Frontend: http://localhost:3000"
echo "- API Docs: http://localhost:8001/docs"
echo ""
echo "📝 Demo Accounts:"
echo "- Athlete: demo_athlete / demo123"
echo "- Scout: demo_scout / demo123"
echo "- Fan: demo_fan / demo123"
echo "- Test: testuser / password"