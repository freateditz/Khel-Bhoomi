# Khel Bhoomi - Local Development Setup

A complete sports social platform with FastAPI backend, React frontend, and MongoDB database.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Node.js 16+
- MongoDB 4.4+
- Git

## 📋 Complete Local Setup Guide

### 1. Clone/Download Project Files

Make sure you have all the project files in a directory structure like:
```
khel-bhoomi/
├── backend/
│   ├── server.py
│   ├── requirements.txt
│   ├── .env.example
│   └── create_dummy_users.py
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── .env.example
│   └── ...
├── docker-compose.yml
├── setup_local.py
└── LOCAL_SETUP_README.md
```

### 2. Database Setup

#### Option A: Using Docker (Recommended)
```bash
# Start MongoDB with Docker
docker-compose up -d mongodb
```

#### Option B: Install MongoDB Locally

**Windows:**
1. Download MongoDB Community Server from https://www.mongodb.com/try/download/community
2. Install and start MongoDB service
3. MongoDB will run on `mongodb://localhost:27017`

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and customize
cp .env.example .env
# Edit .env file with your local settings

# Create dummy users and sample data
python create_dummy_users.py

# Start backend server
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

Backend will be available at: http://localhost:8001
API Documentation: http://localhost:8001/docs

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
# or with yarn:
yarn install

# Copy environment file and customize
cp .env.example .env
# Edit .env file to point to local backend

# Start frontend development server
npm start
# or with yarn:
yarn start
```

Frontend will be available at: http://localhost:3000

### 5. Test the Application

1. Open http://localhost:3000 in your browser
2. Click "Login" in the top navigation
3. Use demo credentials:
   - **Athlete**: demo_athlete / demo123
   - **Scout**: demo_scout / demo123
   - **Fan**: demo_fan / demo123
   - **Test User**: testuser / password

## 🔧 Configuration

### Backend Environment Variables (.env)
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=khel_bhoomi_local
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
```

### Frontend Environment Variables (.env)
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🐳 Docker Setup (Alternative)

For a complete containerized setup:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8001
- MongoDB: localhost:27017

## 🧪 Testing the API

### Test Authentication
```bash
# Login test
curl -X POST "http://localhost:8001/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "demo_athlete", "password": "demo123"}'

# Get user profile (replace TOKEN with actual token from login)
curl -X GET "http://localhost:8001/api/users/me" \
  -H "Authorization: Bearer TOKEN"

# Get posts
curl -X GET "http://localhost:8001/api/posts"
```

## 📁 Project Structure

```
khel-bhoomi/
├── backend/                 # FastAPI backend
│   ├── server.py           # Main application file
│   ├── requirements.txt    # Python dependencies
│   ├── create_dummy_users.py # Database seeding script
│   └── .env               # Environment variables
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   └── components/    # UI components
│   ├── package.json       # Node.js dependencies
│   └── .env              # Environment variables
├── docker-compose.yml     # Docker configuration
└── setup_local.py        # Automated setup script
```

## 🚀 Features

- **Authentication**: JWT-based login/registration
- **User Roles**: Athletes, Scouts, Fans
- **Social Feed**: Post creation, comments, likes
- **User Profiles**: Editable profiles with sports interests
- **Real-time Features**: Live messaging interface
- **Responsive Design**: Mobile-friendly UI

## 🔒 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Athlete | demo_athlete | demo123 |
| Scout | demo_scout | demo123 |
| Fan | demo_fan | demo123 |
| Test User | testuser | password |

## 🛠️ Development

### Backend Development
- FastAPI with automatic API documentation
- Hot reload enabled with `--reload` flag
- MongoDB with Motor (async driver)
- JWT authentication
- CORS enabled for frontend integration

### Frontend Development
- React with hooks
- Tailwind CSS for styling
- Axios for API calls
- React Router for navigation
- Hot reload enabled

## 🐛 Troubleshooting

### Common Issues:

1. **MongoDB Connection Error**
   - Ensure MongoDB is running: `sudo systemctl status mongod`
   - Check connection string in `.env`

2. **Port Already in Use**
   ```bash
   # Kill process on port 8001
   lsof -ti:8001 | xargs kill -9
   # Kill process on port 3000
   lsof -ti:3000 | xargs kill -9
   ```

3. **CORS Errors**
   - Update `CORS_ORIGINS` in backend `.env`
   - Ensure frontend URL matches CORS settings

4. **JWT Token Issues**
   - Clear browser localStorage
   - Check JWT_SECRET_KEY in backend `.env`

5. **Module Import Errors**
   - Ensure virtual environment is activated
   - Reinstall requirements: `pip install -r requirements.txt`

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure all environment variables are set correctly
4. Check console/terminal logs for error messages

## 🎯 Next Steps

Once you have the local setup running:
- Explore the API documentation at http://localhost:8001/docs
- Customize the frontend styling and components
- Add new features or modify existing ones
- Set up your own MongoDB database schema
- Deploy to your preferred cloud platform

Enjoy building with Khel Bhoomi! 🏆