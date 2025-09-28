# Khel Bhoomi - Complete Installation Guide

## 📮 Table of Contents
1. [Quick Setup (Automated)](#quick-setup-automated)
2. [Manual Setup](#manual-setup)
3. [Docker Setup](#docker-setup)
4. [Troubleshooting](#troubleshooting)
5. [Development Tips](#development-tips)

---

## 🚀 Quick Setup (Automated)

The easiest way to get started:

### 1. Download/Clone the Project
```bash
# If you have git
git clone <repository-url>
cd khel-bhoomi

# Or download and extract the ZIP file
```

### 2. Run Automated Setup
```bash
# This will set up everything automatically
python setup_local.py
```

### 3. Start the Application
**On Windows:**
```bash
start.bat
```

**On macOS/Linux:**
```bash
./start.sh
```

### 4. Open in Browser
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Documentation: http://localhost:8001/docs

---

## 🔧 Manual Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB 4.4+

### Step 1: Database Setup

#### Install MongoDB

**Windows:**
1. Download from https://www.mongodb.com/try/download/community
2. Install and start the service

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

### Step 2: Backend Setup

```bash
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

# Create environment file
cp .env.example .env
# Edit .env file with your settings

# Create dummy users
python create_dummy_users.py

# Start backend server
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
# or with yarn:
yarn install

# Create environment file
cp .env.example .env
# Edit .env file if needed

# Start frontend server
npm start
# or with yarn:
yarn start
```

---

## 🐳 Docker Setup

For a containerized setup:

### 1. Prerequisites
- Docker
- Docker Compose

### 2. Start All Services
```bash
docker-compose up -d
```

### 3. View Logs
```bash
docker-compose logs -f
```

### 4. Stop Services
```bash
docker-compose down
```

### 5. Rebuild After Changes
```bash
docker-compose up --build
```

---

## 🔒 Demo Credentials

Use these credentials to test the application:

| Role | Username | Password |
|------|----------|----------|
| Athlete | `demo_athlete` | `demo123` |
| Scout | `demo_scout` | `demo123` |
| Fan | `demo_fan` | `demo123` |
| Test User | `testuser` | `password` |

---

## 🐛 Troubleshooting

### Common Issues

#### 1. MongoDB Connection Error
```
Motor: Could not connect to MongoDB
```
**Solution:**
- Ensure MongoDB is running: `sudo systemctl status mongod`
- Check connection string in backend/.env
- Try: `mongod --dbpath /path/to/data/directory`

#### 2. Port Already in Use
```
Address already in use: 8001
```
**Solution:**
```bash
# Kill process on port 8001
lsof -ti:8001 | xargs kill -9
# Or for port 3000
lsof -ti:3000 | xargs kill -9
```

#### 3. Python Virtual Environment Issues
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:**
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

#### 4. Node.js Dependencies Issues
```
Module not found errors
```
**Solution:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 5. CORS Errors in Browser
```
CORS policy: No 'Access-Control-Allow-Origin' header
```
**Solution:**
- Update `CORS_ORIGINS` in backend/.env
- Ensure frontend URL matches CORS settings

#### 6. JWT Token Issues
```
Unauthorized 401 errors
```
**Solution:**
- Clear browser localStorage
- Check JWT_SECRET_KEY in backend/.env
- Ensure same secret key across restarts

### Debug Mode

Enable detailed logging:

**Backend:**
```bash
# Add to backend/.env
DEBUG=true
LOG_LEVEL=debug
```

**Frontend:**
```bash
# Add to frontend/.env
REACT_APP_DEBUG_MODE=true
```

---

## 🛠️ Development Tips

### Hot Reload
- Backend: Automatic with `--reload` flag
- Frontend: Automatic with React dev server

### API Testing
- Use the built-in docs: http://localhost:8001/docs
- Test with curl:
```bash
curl -X POST "http://localhost:8001/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "demo_athlete", "password": "demo123"}'
```

### Database Management
```bash
# Connect to MongoDB shell
mongo

# Switch to your database
use khel_bhoomi_local

# View collections
show collections

# View users
db.users.find().pretty()

# View posts
db.posts.find().pretty()
```

### File Structure
```
khel-bhoomi/
├── backend/
│   ├── server.py              # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── create_dummy_users.py  # Database seeding
│   ├── .env                   # Environment variables
│   └── venv/                  # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   └── components/        # UI components
│   ├── package.json           # Node.js dependencies
│   ├── .env                   # Environment variables
│   └── node_modules/          # Node.js modules
├── docker-compose.yml         # Docker configuration
├── setup_local.py            # Automated setup script
├── start.sh / start.bat      # Start scripts
└── LOCAL_SETUP_README.md     # Detailed instructions
```

### Environment Variables Reference

**Backend (.env):**
- `MONGO_URL`: MongoDB connection string
- `DB_NAME`: Database name
- `CORS_ORIGINS`: Allowed frontend origins
- `JWT_SECRET_KEY`: Secret for JWT tokens

**Frontend (.env):**
- `REACT_APP_BACKEND_URL`: Backend API URL
- `WDS_SOCKET_PORT`: WebSocket port for hot reload

---

## 🎆 Next Steps

Once you have the application running:

1. **Explore the Features:**
   - Create posts as different user types
   - Test the messaging system
   - Try profile editing

2. **Customize:**
   - Modify the UI components
   - Add new API endpoints
   - Change the styling

3. **Extend:**
   - Add real-time features with WebSockets
   - Implement file uploads
   - Add email notifications

4. **Deploy:**
   - Use platforms like Heroku, DigitalOcean, or AWS
   - Set up CI/CD pipelines
   - Configure production databases

Enjoy building with Khel Bhoomi! 🏆