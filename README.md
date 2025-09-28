# 🏆 Khel Bhoomi - Sports Social Platform

*Where athletes shine, scouts discover champions, and fans celebrate the spirit of sports.*

## 🌟 Overview

Khel Bhoomi is a comprehensive sports social platform built with modern web technologies. It connects athletes, scouts, and fans in India's most vibrant sports community, providing features for networking, talent discovery, and sports engagement.

## ⚡ Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
python setup_local.py

# Start the application
./start.sh        # macOS/Linux
start.bat         # Windows
```

### Option 2: Docker (Easiest)
```bash
docker-compose up -d
```

### Option 3: Manual Setup
See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for detailed instructions.

## 📍 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

## 🔒 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| 🏅 Athlete | `demo_athlete` | `demo123` |
| 🕵️ Scout | `demo_scout` | `demo123` |
| ❤️ Fan | `demo_fan` | `demo123` |
| 🧪 Test User | `testuser` | `password` |

## 🚀 Features

### 🏅 For Athletes
- **Profile Showcase**: Display achievements, stats, and sports interests
- **Content Sharing**: Post training updates, achievements, and media
- **Network Building**: Connect with scouts and other athletes
- **Achievement Tracking**: Maintain a record of accomplishments

### 🕵️ For Scouts
- **Talent Discovery**: Browse and discover promising athletes
- **Advanced Search**: Filter athletes by sports, location, and performance
- **Direct Communication**: Message athletes directly
- **Portfolio Management**: Save and track potential recruits

### ❤️ For Fans
- **Community Engagement**: Follow favorite athletes and teams
- **Content Consumption**: Stay updated with sports news and updates
- **Social Interaction**: Comment, like, and share sports content
- **Event Following**: Track tournaments and competitions

### 📱 Core Platform Features
- **Real-time Feed**: Dynamic sports content stream
- **Messaging System**: Direct communication between users
- **Multi-sport Support**: Cricket, Basketball, Football, Tennis, and more
- **Role-based Access**: Tailored experiences for different user types
- **Responsive Design**: Mobile-first, cross-platform compatibility

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for flexible data storage
- **Motor**: Async MongoDB driver
- **JWT**: Secure authentication
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for FastAPI

### Frontend
- **React**: Modern JavaScript library for UI
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **React Router**: Client-side routing
- **Lucide React**: Beautiful icons

### Database
- **MongoDB**: Document-based NoSQL database
- **Collections**: Users, Posts, Messages, Comments
- **Indexing**: Optimized queries for performance

## 📋 Project Structure

```
khel-bhoomi/
├── 💾 backend/                 # FastAPI backend application
│   ├── server.py               # Main application file
│   ├── requirements.txt        # Python dependencies
│   ├── create_dummy_users.py   # Database seeding script
│   ├── .env                    # Environment variables
│   └── Dockerfile             # Docker configuration
├── 🖄️ frontend/                # React frontend application
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   └── components/         # Reusable UI components
│   ├── package.json            # Node.js dependencies
│   ├── .env                    # Environment variables
│   └── Dockerfile             # Docker configuration
├── 🐳 docker-compose.yml        # Multi-container Docker app
├── 🛠️ setup_local.py           # Automated setup script
├── 🚀 start.sh / start.bat     # Application start scripts
├── 📝 LOCAL_SETUP_README.md   # Detailed setup instructions
└── 📋 INSTALLATION_GUIDE.md   # Complete installation guide
```

## 📚 API Documentation

Once the backend is running, visit http://localhost:8001/docs for interactive API documentation powered by FastAPI's automatic OpenAPI generation.

### Key Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile

#### Posts & Social Features
- `GET /api/posts` - Get posts feed
- `POST /api/posts` - Create new post
- `POST /api/posts/{id}/like` - Like/unlike post
- `GET /api/posts/{id}/comments` - Get post comments
- `POST /api/posts/{id}/comments` - Add comment

## 🔧 Development

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB 4.4+
- Git

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd khel-bhoomi
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   cp .env.example .env
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   ```

4. **Database Setup**
   ```bash
   # Start MongoDB
   sudo systemctl start mongod  # Linux
   brew services start mongodb/brew/mongodb-community  # macOS
   
   # Create dummy data
   cd backend
   python create_dummy_users.py
   ```

### Running in Development Mode

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

### Testing

**Backend Tests:**
```bash
cd backend
python -m pytest
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

**API Testing:**
```bash
# Test login
curl -X POST "http://localhost:8001/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "demo_athlete", "password": "demo123"}'
```

## 🐳 Docker Development

### Quick Start
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Development with Docker
```bash
# Rebuild after code changes
docker-compose up --build

# Run specific service
docker-compose up mongodb backend
```

## 🛡️ Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **CORS Protection**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic models for request validation
- **Environment Variables**: Sensitive data stored in environment files

## 📊 Performance Optimizations

- **Async/Await**: Non-blocking I/O operations
- **Database Indexing**: Optimized MongoDB queries
- **Hot Reload**: Fast development iteration
- **Component Optimization**: React hooks and memoization
- **Lazy Loading**: Code splitting for faster initial load

## 🌎 Deployment

### Production Checklist
- [ ] Update JWT_SECRET_KEY in production
- [ ] Configure production MongoDB instance
- [ ] Set up SSL/TLS certificates
- [ ] Configure environment variables
- [ ] Set up monitoring and logging
- [ ] Configure backup strategies

### Deployment Options
- **Heroku**: Easy deployment with Heroku CLI
- **DigitalOcean**: App Platform or Droplets
- **AWS**: EC2, ECS, or Lambda
- **Vercel**: Frontend deployment
- **Railway**: Full-stack deployment

## 🐛 Troubleshooting

Common issues and solutions:

1. **MongoDB Connection**: Ensure MongoDB is running and connection string is correct
2. **Port Conflicts**: Use `lsof -ti:PORT | xargs kill -9` to free up ports
3. **Dependencies**: Delete `node_modules` and `venv`, then reinstall
4. **CORS Issues**: Update `CORS_ORIGINS` in backend environment
5. **Authentication**: Clear browser localStorage and check JWT secret

For detailed troubleshooting, see [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md#troubleshooting).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with descriptive messages: `git commit -m "Add new feature"`
5. Push to your branch: `git push origin feature-name`
6. Create a Pull Request

### Code Style
- **Backend**: Follow PEP 8 guidelines
- **Frontend**: Use Prettier and ESLint configurations
- **Database**: Use descriptive field names and proper indexing

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Support

For support and questions:
- Create an issue on GitHub
- Check the [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- Review the [troubleshooting section](#troubleshooting)

## 🗺️ Roadmap

### Upcoming Features
- [ ] Real-time messaging with WebSockets
- [ ] Advanced search and filtering
- [ ] File upload and media management
- [ ] Email notifications
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Integration with sports APIs
- [ ] Multi-language support

### Version History
- **v1.0.0**: Initial release with core features
- **v1.1.0**: Enhanced UI and performance improvements (planned)
- **v2.0.0**: Real-time features and mobile app (planned)

---

**Built with ❤️ for the sports community in India**

*Khel Bhoomi - Empowering athletes, connecting scouts, and celebrating sports!* 🏆