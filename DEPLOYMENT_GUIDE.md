# Khel Bhoomi - Deployment Guide for Render.com

## Prerequisites

1. **GitHub Repository**: Push your code to GitHub
2. **MongoDB Atlas Account**: Create a free MongoDB Atlas cluster
3. **Render Account**: Sign up at [render.com](https://render.com)

## Step-by-Step Deployment Guide

### Phase 1: Prepare Your MongoDB Database

1. **Create MongoDB Atlas Cluster**:
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a free account and cluster
   - Create a database user with read/write permissions
   - Whitelist IP addresses (use `0.0.0.0/0` for all IPs or specific IPs)
   - Get your connection string: `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/`

2. **Create Database Collections**:
   - Database name: `Khelbhoomi`
   - Collections to create:
     - `users`
     - `login` 
     - `signup`
     - `posts`
     - `profile`
     - `comments`
     - `likes`
     - `follows`
     - `messages`
     - `Data` (for backward compatibility)

### Phase 2: Deploy Backend (Web Service)

1. **Connect GitHub to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository containing your code

2. **Backend Configuration**:
   ```
   Name: khel-bhoomi-backend
   Environment: Python 3
   Region: Choose closest to your users
   Branch: main (or your default branch)
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   ```

3. **Environment Variables** (Add these in Render dashboard):
   ```
   MONGO_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
   DB_NAME=Khelbhoomi
   JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-12345
   CORS_ORIGINS=https://your-frontend-domain.onrender.com
   HOST=0.0.0.0
   PORT=10000
   ENVIRONMENT=production
   ```

4. **Deploy Backend**:
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note your backend URL: `https://your-service-name.onrender.com`

### Phase 3: Deploy Frontend (Static Site)

1. **Create Static Site**:
   - In Render Dashboard: "New +" → "Static Site"
   - Select same GitHub repository
   - Configure:
     ```
     Name: khel-bhoomi-frontend
     Branch: main
     Root Directory: frontend
     Build Command: yarn install && yarn build
     Publish Directory: dist
     ```

2. **Environment Variables for Frontend**:
   ```
   VITE_BACKEND_URL=https://your-backend-service-name.onrender.com
   ```

3. **Deploy Frontend**:
   - Click "Create Static Site"
   - Wait for build and deployment
   - Your frontend will be available at: `https://your-frontend-name.onrender.com`

### Phase 4: Update Backend CORS

1. **Update Backend Environment**:
   - Go to your backend service in Render
   - Update `CORS_ORIGINS` environment variable:
     ```
     CORS_ORIGINS=https://your-frontend-name.onrender.com
     ```
   - Deploy the backend again

### Phase 5: Initialize Database with Demo Users

1. **Create Demo Users Script**:
   - Use the provided `create_demo_users_new.py` script
   - Update MongoDB connection string in the script
   - Run it locally or create a separate one-time job in Render

2. **Manual Database Setup** (Alternative):
   - Connect to MongoDB Atlas directly
   - Import demo users data manually

## Local Development Setup

### Backend Local Setup:

1. **Clone and Setup**:
   ```bash
   git clone your-repo-url
   cd your-repo/backend
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   ```bash
   # Copy and edit environment file
   cp .env.example .env
   
   # Edit .env file with your local MongoDB and settings:
   MONGO_URL=mongodb+srv://your-atlas-connection-string
   DB_NAME=Khelbhoomi
   JWT_SECRET_KEY=your-local-secret-key
   CORS_ORIGINS=http://localhost:3000
   HOST=0.0.0.0
   PORT=8001
   ENVIRONMENT=development
   ```

3. **Run Backend**:
   ```bash
   python main.py
   ```
   - API will be available at: http://localhost:8001
   - API docs: http://localhost:8001/docs

### Frontend Local Setup:

1. **Setup Frontend**:
   ```bash
   cd your-repo/frontend
   
   # Install dependencies
   yarn install
   ```

2. **Environment Configuration**:
   ```bash
   # Copy and edit environment file
   cp .env.example .env
   
   # Edit .env file:
   VITE_BACKEND_URL=http://localhost:8001
   WDS_SOCKET_PORT=443
   ```

3. **Run Frontend**:
   ```bash
   yarn dev
   ```
   - Frontend will be available at: http://localhost:3000

## Important Notes

### Security:
- Always use strong JWT secret keys in production
- Restrict CORS origins to your actual frontend domain
- Use environment variables for all sensitive data
- Enable MongoDB Atlas IP whitelisting for better security

### Performance:
- Render free tier has limitations (services sleep after 15 minutes of inactivity)
- Consider upgrading to paid plans for production use
- MongoDB Atlas free tier has 512MB storage limit

### Demo Accounts:
After deployment, these demo accounts will be available:
- **Athlete**: `demo_athlete` / `demo123`
- **Scout**: `demo_scout` / `demo123`
- **Fan**: `demo_fan` / `demo123`
- **Test User**: `testuser` / `password`

## Troubleshooting

### Common Issues:
1. **CORS Errors**: Update `CORS_ORIGINS` in backend environment variables
2. **Database Connection**: Verify MongoDB connection string and network access
3. **Build Failures**: Check build logs in Render dashboard
4. **Environment Variables**: Ensure all required variables are set correctly

### Logs Access:
- Backend logs: Available in Render service dashboard
- Frontend build logs: Available in Render static site dashboard
- MongoDB logs: Available in Atlas dashboard

## Support
For issues with deployment, check:
1. Render build and runtime logs
2. MongoDB Atlas connection and security settings
3. Environment variable configuration
4. Network and CORS settings