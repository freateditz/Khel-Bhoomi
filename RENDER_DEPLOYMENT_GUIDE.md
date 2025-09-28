# Khel Bhoomi - Render Deployment Guide

## Overview
This guide will help you deploy the Khel Bhoomi sports platform to Render with both backend and frontend services.

## Prerequisites

### 1. MongoDB Atlas Setup (Required)
- Create a MongoDB Atlas account at https://www.mongodb.com/atlas
- Create a new cluster (free tier available)
- Create a database user with read/write permissions
- Get your connection string (mongodb+srv://...)
- Whitelist Render IP addresses (or use 0.0.0.0/0 for all IPs)

### 2. Render Account
- Create account at https://render.com
- Connect your GitHub repository

## Deployment Steps

### Option 1: Automated Deployment (Recommended)
1. **Fork/Upload Repository**
   - Upload this entire project to your GitHub repository
   - Ensure all files including `render.yaml` are included

2. **Deploy to Render**
   - Go to Render Dashboard
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing this project
   - Render will automatically detect the `render.yaml` file

3. **Configure Environment Variables**
   - In Backend service settings, add:
     ```
     MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
     JWT_SECRET_KEY=generate-a-secure-32-character-secret-key
     ```

### Option 2: Manual Deployment

#### Step 1: Deploy Backend
1. **Create Web Service**
   - Service Type: Web Service
   - Environment: Python 3
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT`

2. **Set Environment Variables**
   ```
   MONGO_URL=mongodb+srv://your-connection-string
   DB_NAME=Khelbhoomi
   JWT_SECRET_KEY=your-secure-secret-key-32-chars-minimum
   CORS_ORIGINS=*
   ENVIRONMENT=production
   HOST=0.0.0.0
   ```

3. **Deploy Backend**
   - Save and deploy
   - Note the backend service URL (e.g., https://khel-bhoomi-backend.onrender.com)

#### Step 2: Deploy Frontend
1. **Create Web Service**
   - Service Type: Web Service  
   - Environment: Node.js
   - Build Command: `cd frontend && yarn install && yarn build`
   - Start Command: `cd frontend && yarn preview --host 0.0.0.0 --port $PORT`

2. **Set Environment Variables**
   ```
   VITE_BACKEND_URL=https://your-backend-service.onrender.com
   NODE_ENV=production
   ```

3. **Deploy Frontend**
   - Save and deploy
   - Your app will be available at the frontend service URL

## Required Environment Variables

### Backend (.env)
```env
# Database (REQUIRED)
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=Khelbhoomi

# Security (REQUIRED)  
JWT_SECRET_KEY=your-secure-secret-key-minimum-32-characters

# Server Configuration
CORS_ORIGINS=*
HOST=0.0.0.0
PORT=10000
ENVIRONMENT=production
```

### Frontend (.env)
```env
# API Configuration (REQUIRED)
VITE_BACKEND_URL=https://your-backend-service.onrender.com

# Build Configuration  
NODE_ENV=production
```

## Post-Deployment Setup

### 1. Initialize Database with Demo Users
After successful deployment, the demo users will be available:
- **Demo Athlete**: `demo_athlete` / `demo123`
- **Demo Scout**: `demo_scout` / `demo123`  
- **Demo Fan**: `demo_fan` / `demo123`
- **Test User**: `testuser` / `password`

### 2. Verify Deployment
- Visit your frontend URL
- Test login with demo credentials
- Check backend API at `https://your-backend-url/docs`

### 3. Update CORS Origins (Recommended)
- Replace `CORS_ORIGINS=*` with your actual frontend domain:
  ```
  CORS_ORIGINS=https://your-frontend-service.onrender.com
  ```

## Troubleshooting

### Common Issues

#### 1. Database Connection Error
- Verify MongoDB Atlas connection string
- Check database user permissions
- Ensure IP addresses are whitelisted

#### 2. Backend Service Not Starting
- Check build logs in Render dashboard
- Verify all required environment variables are set
- Ensure requirements.txt is complete

#### 3. Frontend Can't Connect to Backend
- Verify `VITE_BACKEND_URL` is set correctly
- Check CORS configuration in backend
- Ensure backend service is running

#### 4. Authentication Issues
- Verify `JWT_SECRET_KEY` is at least 32 characters
- Check MongoDB collections are populated with demo users

### Support
- Check Render service logs for detailed error messages
- Review MongoDB Atlas logs for database issues
- Verify all environment variables match the required format

## Cost Estimation
- **Free Tier**: Both services can run on Render's free tier with limitations
- **Paid Plans**: Starter plan ($7/month per service) recommended for production

## Performance Optimization
- Consider upgrading to paid plans for better performance
- Use MongoDB Atlas M10+ cluster for production
- Enable caching and CDN for static assets

## Security Recommendations
- Use strong, unique JWT secret key
- Restrict CORS origins to your domain only
- Enable MongoDB Atlas IP whitelisting
- Use environment variables for all sensitive data