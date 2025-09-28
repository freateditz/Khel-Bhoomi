# Khel Bhoomi - Sports Social Platform

A comprehensive sports social platform connecting athletes, scouts, and fans. Built with FastAPI backend and React frontend.

## 🌟 Features

- **Multi-Role System**: Athletes, Scouts, and Fans with tailored experiences
- **Authentication**: Secure JWT-based login/signup system
- **Social Feed**: Post updates, achievements, and sports content
- **Profile Management**: Comprehensive user profiles with sports interests
- **Real-time Features**: Comments, likes, and social interactions
- **Demo Accounts**: Ready-to-use accounts for testing

## 🚀 Quick Start

### Option 1: Local Development

**Prerequisites:**
- Python 3.11+
- Node.js 18+
- Yarn package manager
- MongoDB Atlas account (or local MongoDB)

**Setup:**
```bash
# Clone the repository
git clone <your-repo-url>
cd khel-bhoomi

# Run setup script (Linux/Mac)
./setup-local.sh

# Or on Windows
setup-local.bat
```

**Manual Setup:**
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings

# Frontend setup  
cd ../frontend
yarn install
cp .env.example .env
# Edit .env with backend URL
```

**Start Development Servers:**
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py

# Terminal 2 - Frontend
cd frontend
yarn dev
```

### Option 2: Deploy on Render

See the complete [Deployment Guide](DEPLOYMENT_GUIDE.md) for step-by-step Render deployment instructions.

## 🔧 Configuration

### Backend Environment Variables (.env)
```env
MONGO_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
DB_NAME=Khelbhoomi
JWT_SECRET_KEY=your-super-secret-jwt-key
CORS_ORIGINS=http://localhost:3000
HOST=0.0.0.0
PORT=8001
ENVIRONMENT=development
```

### Frontend Environment Variables (.env)
```env
VITE_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=443
```

## 📊 Database Structure

The application uses MongoDB with the following collections:

- **users** - User accounts and authentication data
- **login** - Login attempt records and analytics
- **signup** - User registration records
- **posts** - User posts and social content
- **profile** - Extended user profile information
- **comments** - Post comments and interactions
- **likes** - Post likes and reactions
- **follows** - User follow relationships
- **messages** - Direct messaging between users

## 🎯 Demo Accounts

Ready-to-use demo accounts for testing:

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| Athlete | `demo_athlete` | `demo123` | Professional athlete account |
| Scout | `demo_scout` | `demo123` | Sports scout account |
| Fan | `demo_fan` | `demo123` | Sports fan account |
| Test | `testuser` | `password` | General test account |

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login

### Users
- `GET /api/users/me` - Get current user profile
- `GET /api/users/{username}` - Get user by username
- `PUT /api/users/me` - Update user profile

### Posts
- `GET /api/posts` - Get all posts
- `POST /api/posts` - Create new post
- `GET /api/posts/user/{user_id}` - Get posts by user

### System
- `GET /api/health` - Health check endpoint

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - Document database with Motor async driver
- **JWT** - Secure authentication tokens
- **Uvicorn** - ASGI server for production
- **Pydantic** - Data validation and serialization

### Frontend
- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Tailwind CSS** - Utility-first CSS framework
- **Shadcn/ui** - Beautiful UI components
- **Lucide React** - Modern icon library

## 🚀 Deployment

### Render.com Deployment

1. **Prepare MongoDB Atlas**
   - Create free cluster at [MongoDB Atlas](https://cloud.mongodb.com)
   - Create database user and get connection string
   - Whitelist IP addresses

2. **Deploy Backend (Web Service)**
   - Connect GitHub repository to Render
   - Configure as Python web service
   - Set environment variables
   - Deploy with `python main.py` command

3. **Deploy Frontend (Static Site)**
   - Configure as static site
   - Build command: `yarn install && yarn build`
   - Publish directory: `dist`
   - Set `VITE_BACKEND_URL` environment variable

4. **Update CORS Settings**
   - Update backend `CORS_ORIGINS` with frontend URL
   - Redeploy backend service

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 🛠️ Development

### Project Structure
```
khel-bhoomi/
├── backend/                 # FastAPI backend
│   ├── server.py           # Main FastAPI application
│   ├── main.py             # Server startup script
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment template
│   └── Dockerfile.new      # Docker configuration
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   └── components/     # UI components
│   ├── package.json        # Node.js dependencies
│   ├── vite.config.js      # Vite configuration
│   ├── .env.example        # Environment template
│   └── Dockerfile.new      # Docker configuration
├── DEPLOYMENT_GUIDE.md     # Detailed deployment guide
├── setup-local.sh          # Local setup script (Linux/Mac)
├── setup-local.bat         # Local setup script (Windows)
└── README.md              # This file
```

## 📝 Demo Accounts

Ready-to-use demo accounts for testing:
- **Athlete**: `demo_athlete` / `demo123`
- **Scout**: `demo_scout` / `demo123`
- **Fan**: `demo_fan` / `demo123`
- **Test User**: `testuser` / `password`

## 🆘 Support & Troubleshooting

### Common Issues
1. **CORS Errors**: Check `CORS_ORIGINS` in backend environment
2. **Database Connection**: Verify MongoDB connection string
3. **Environment Variables**: Ensure all required vars are set
4. **Build Issues**: Check Node.js and Python versions

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)