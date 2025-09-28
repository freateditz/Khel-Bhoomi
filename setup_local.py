#!/usr/bin/env python3
"""
Automated Local Setup Script for Khel Bhoomi
This script helps set up the development environment automatically.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class KhelBhoomiSetup:
    def __init__(self):
        self.project_root = Path.cwd()
        self.backend_dir = self.project_root / 'backend'
        self.frontend_dir = self.project_root / 'frontend'
        
    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f" {text}")
        print(f"{'='*60}")
        
    def print_step(self, text):
        print(f"\n🔄 {text}...")
        
    def print_success(self, text):
        print(f"✅ {text}")
        
    def print_error(self, text):
        print(f"❌ {text}")
        
    def check_prerequisites(self):
        self.print_header("Checking Prerequisites")
        
        # Check Python
        try:
            python_version = sys.version_info
            if python_version >= (3, 8):
                self.print_success(f"Python {python_version.major}.{python_version.minor} found")
            else:
                self.print_error("Python 3.8+ required")
                return False
        except:
            self.print_error("Python not found")
            return False
            
        # Check Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                self.print_success(f"Node.js {result.stdout.strip()} found")
            else:
                self.print_error("Node.js not found - install from https://nodejs.org/")
                return False
        except:
            self.print_error("Node.js not found - install from https://nodejs.org/")
            return False
            
        # Check MongoDB (optional - can use Docker)
        try:
            result = subprocess.run(['mongod', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                self.print_success("MongoDB found")
            else:
                print("⚠️  MongoDB not found locally - Docker option available")
        except:
            print("⚠️  MongoDB not found locally - Docker option available")
            
        return True
        
    def setup_backend(self):
        self.print_header("Setting Up Backend")
        
        if not self.backend_dir.exists():
            self.print_error("Backend directory not found")
            return False
            
        os.chdir(self.backend_dir)
        
        # Create virtual environment
        self.print_step("Creating Python virtual environment")
        try:
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
            self.print_success("Virtual environment created")
        except subprocess.CalledProcessError:
            self.print_error("Failed to create virtual environment")
            return False
            
        # Determine activation script
        if os.name == 'nt':  # Windows
            activate_script = 'venv\\Scripts\\activate'
            pip_cmd = 'venv\\Scripts\\pip'
            python_cmd = 'venv\\Scripts\\python'
        else:  # Unix/Linux/macOS
            activate_script = 'source venv/bin/activate'
            pip_cmd = 'venv/bin/pip'
            python_cmd = 'venv/bin/python'
            
        # Install requirements
        self.print_step("Installing Python dependencies")
        try:
            subprocess.run([pip_cmd, 'install', '-r', 'requirements.txt'], check=True)
            self.print_success("Dependencies installed")
        except subprocess.CalledProcessError:
            self.print_error("Failed to install dependencies")
            return False
            
        # Create .env file if it doesn't exist
        env_file = self.backend_dir / '.env'
        if not env_file.exists():
            self.print_step("Creating backend .env file")
            env_content = '''MONGO_URL=mongodb://localhost:27017
DB_NAME=khel_bhoomi_local
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
JWT_SECRET_KEY=khel-bhoomi-super-secret-local-key-change-in-production
'''
            env_file.write_text(env_content)
            self.print_success("Backend .env file created")
            
        # Create dummy users
        self.print_step("Creating dummy users and sample data")
        try:
            subprocess.run([python_cmd, 'create_dummy_users.py'], check=True)
            self.print_success("Dummy users created")
        except subprocess.CalledProcessError:
            print("⚠️  Could not create dummy users - you may need to start MongoDB first")
            
        os.chdir(self.project_root)
        return True
        
    def setup_frontend(self):
        self.print_header("Setting Up Frontend")
        
        if not self.frontend_dir.exists():
            self.print_error("Frontend directory not found")
            return False
            
        os.chdir(self.frontend_dir)
        
        # Install npm dependencies
        self.print_step("Installing Node.js dependencies")
        try:
            # Try yarn first, fallback to npm
            result = subprocess.run(['yarn', '--version'], capture_output=True)
            if result.returncode == 0:
                subprocess.run(['yarn', 'install'], check=True)
                self.print_success("Dependencies installed with Yarn")
            else:
                subprocess.run(['npm', 'install'], check=True)
                self.print_success("Dependencies installed with npm")
        except subprocess.CalledProcessError:
            self.print_error("Failed to install frontend dependencies")
            return False
            
        # Create .env file if it doesn't exist
        env_file = self.frontend_dir / '.env'
        if not env_file.exists():
            self.print_step("Creating frontend .env file")
            env_content = '''REACT_APP_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=443
'''
            env_file.write_text(env_content)
            self.print_success("Frontend .env file created")
            
        os.chdir(self.project_root)
        return True
        
    def create_docker_compose(self):
        self.print_header("Creating Docker Compose Configuration")
        
        docker_compose_content = '''version: '3.8'

services:
  mongodb:
    image: mongo:4.4
    container_name: khel_bhoomi_mongo
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: khel_bhoomi_local

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: khel_bhoomi_backend
    restart: unless-stopped
    ports:
      - "8001:8001"
    environment:
      - MONGO_URL=mongodb://mongodb:27017
      - DB_NAME=khel_bhoomi_local
      - CORS_ORIGINS=http://localhost:3000
      - JWT_SECRET_KEY=khel-bhoomi-docker-secret-key
    depends_on:
      - mongodb
    volumes:
      - ./backend:/app
    command: uvicorn server:app --host 0.0.0.0 --port 8001 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: khel_bhoomi_frontend
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_BACKEND_URL=http://localhost:8001
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm start

volumes:
  mongodb_data:
'''
        
        docker_file = self.project_root / 'docker-compose.yml'
        docker_file.write_text(docker_compose_content)
        self.print_success("Docker Compose configuration created")
        
    def create_dockerfiles(self):
        # Backend Dockerfile
        backend_dockerfile = '''FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
'''
        
        (self.backend_dir / 'Dockerfile').write_text(backend_dockerfile)
        
        # Frontend Dockerfile
        frontend_dockerfile = '''FROM node:16-alpine

WORKDIR /app

COPY package.json yarn.lock* ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
'''
        
        (self.frontend_dir / 'Dockerfile').write_text(frontend_dockerfile)
        
    def create_start_scripts(self):
        self.print_header("Creating Start Scripts")
        
        # Unix/Linux/macOS start script
        start_script_unix = '''#!/bin/bash

echo "🚀 Starting Khel Bhoomi Development Server"
echo "======================================"

# Start MongoDB if not running
if ! pgrep -x "mongod" > /dev/null; then
    echo "Starting MongoDB..."
    sudo systemctl start mongod 2>/dev/null || mongod --fork --logpath /var/log/mongodb.log --dbpath /var/lib/mongodb 2>/dev/null || echo "Please start MongoDB manually"
fi

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Khel Bhoomi is starting up!"
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend: http://localhost:8001"
echo "📍 API Docs: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user interrupt
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
'''
        
        # Windows start script
        start_script_windows = '''@echo off
echo 🚀 Starting Khel Bhoomi Development Server
echo ======================================

REM Start backend
echo Starting backend server...
cd backend
call venv\\Scripts\\activate
start "Khel Bhoomi Backend" uvicorn server:app --host 0.0.0.0 --port 8001 --reload
cd ..

REM Wait a bit
timeout /t 3 /nobreak > nul

REM Start frontend
echo Starting frontend server...
cd frontend
start "Khel Bhoomi Frontend" npm start
cd ..

echo.
echo ✅ Khel Bhoomi is starting up!
echo 📍 Frontend: http://localhost:3000
echo 📍 Backend: http://localhost:8001
echo 📍 API Docs: http://localhost:8001/docs
echo.
echo Close the terminal windows to stop the servers
pause
'''
        
        (self.project_root / 'start.sh').write_text(start_script_unix)
        (self.project_root / 'start.bat').write_text(start_script_windows)
        
        # Make Unix script executable
        if os.name != 'nt':
            os.chmod(self.project_root / 'start.sh', 0o755)
            
        self.print_success("Start scripts created")
        
    def print_completion_message(self):
        self.print_header("Setup Complete! 🎉")
        
        print("\n🚀 Your Khel Bhoomi development environment is ready!")
        print("\n📋 Quick Start:")
        print("   1. Make sure MongoDB is running")
        if os.name == 'nt':
            print("   2. Run: start.bat")
        else:
            print("   2. Run: ./start.sh")
        print("   3. Open http://localhost:3000 in your browser")
        print("   4. Login with demo credentials:")
        print("      - demo_athlete / demo123")
        print("      - demo_scout / demo123")
        print("      - demo_fan / demo123")
        
        print("\n🐳 Alternative Docker Setup:")
        print("   docker-compose up -d")
        
        print("\n📖 For detailed instructions, see LOCAL_SETUP_README.md")
        
        print("\n🎯 URLs:")
        print("   Frontend: http://localhost:3000")
        print("   Backend: http://localhost:8001")
        print("   API Docs: http://localhost:8001/docs")
        
if __name__ == "__main__":
    setup = KhelBhoomiSetup()
    
    if not setup.check_prerequisites():
        print("\n❌ Prerequisites check failed. Please install missing requirements.")
        sys.exit(1)
        
    if not setup.setup_backend():
        print("\n❌ Backend setup failed.")
        sys.exit(1)
        
    if not setup.setup_frontend():
        print("\n❌ Frontend setup failed.")
        sys.exit(1)
        
    setup.create_docker_compose()
    setup.create_dockerfiles()
    setup.create_start_scripts()
    setup.print_completion_message()