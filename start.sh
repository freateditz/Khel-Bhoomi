#!/bin/bash

echo "🚀 Starting Khel Bhoomi Development Server"
echo "======================================"

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "Starting MongoDB..."
    # Try different methods to start MongoDB
    if command -v systemctl &> /dev/null; then
        sudo systemctl start mongod 2>/dev/null || echo "Please start MongoDB manually: sudo systemctl start mongod"
    elif command -v brew &> /dev/null; then
        brew services start mongodb/brew/mongodb-community 2>/dev/null || echo "Please start MongoDB manually: brew services start mongodb/brew/mongodb-community"
    else
        echo "Please start MongoDB manually"
    fi
else
    echo "✅ MongoDB is already running"
fi

# Start backend
echo "Starting backend server..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating backend .env file..."
    cp .env.example .env
fi

# Create dummy users if database is empty
echo "Setting up dummy users..."
python create_dummy_users.py 2>/dev/null || echo "Dummy users already exist or MongoDB not ready"

# Start backend server
uvicorn server:app --host 0.0.0.0 --port 8001 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Start frontend
echo "Starting frontend server..."
cd frontend

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    cp .env.example .env
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    if command -v yarn &> /dev/null; then
        yarn install
    else
        npm install
    fi
fi

# Start frontend server
if command -v yarn &> /dev/null; then
    yarn start &
else
    npm start &
fi
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Khel Bhoomi is starting up!"
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend: http://localhost:8001"
echo "📍 API Docs: http://localhost:8001/docs"
echo ""
echo "🔒 Demo Credentials:"
echo "   - Athlete: demo_athlete / demo123"
echo "   - Scout: demo_scout / demo123"
echo "   - Fan: demo_fan / demo123"
echo ""
echo "Press Ctrl+C to stop all servers"

# Function to cleanup
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "Servers stopped. Goodbye!"
    exit 0
}

# Set trap for cleanup
trap cleanup INT TERM

# Wait for user interrupt
wait