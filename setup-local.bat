@echo off
echo 🚀 Starting Khel Bhoomi Local Development Environment
echo ==================================================

REM Check if we're in the right directory
if not exist "backend" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)
if not exist "frontend" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check dependencies
echo 🔍 Checking dependencies...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18 or higher.
    pause
    exit /b 1
)

yarn --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Yarn is not installed. Please install Yarn package manager.
    pause
    exit /b 1
)

echo ✅ All dependencies found!

REM Setup backend
echo 🔧 Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚙️ Creating backend .env file from template...
    copy .env.example .env
    echo ⚠️ Please edit backend\.env with your MongoDB connection and other settings
)

cd ..

REM Setup frontend
echo 🔧 Setting up frontend...
cd frontend

REM Install Node dependencies
echo 📦 Installing Node.js dependencies...
yarn install

REM Check if .env file exists
if not exist ".env" (
    echo ⚙️ Creating frontend .env file from template...
    copy .env.example .env
    echo ⚠️ Please edit frontend\.env with your backend URL
)

cd ..

echo ✅ Setup complete!
echo.
echo 🚀 To start development:
echo 1. Start backend: cd backend ^&^& venv\Scripts\activate ^&^& python main.py
echo 2. Start frontend: cd frontend ^&^& yarn dev
echo.
echo 🌐 URLs:
echo - Backend: http://localhost:8001
echo - Frontend: http://localhost:3000
echo - API Docs: http://localhost:8001/docs
echo.
echo 📝 Demo Accounts:
echo - Athlete: demo_athlete / demo123
echo - Scout: demo_scout / demo123
echo - Fan: demo_fan / demo123
echo - Test: testuser / password
echo.
pause