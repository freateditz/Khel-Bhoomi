# 🚀 Khel Bhoomi - Render Deployment Checklist

## Pre-Deployment Requirements ✅

### 1. MongoDB Atlas Setup
- [ ] Created MongoDB Atlas account
- [ ] Created cluster (M0 free tier available)
- [ ] Created database user with read/write permissions
- [ ] Whitelisted IP addresses (0.0.0.0/0 for Render)
- [ ] Obtained connection string: `mongodb+srv://username:password@cluster.mongodb.net/`

### 2. Environment Variables
- [ ] Generated secure JWT secret key (32+ characters)
- [ ] Prepared MongoDB connection string
- [ ] Identified frontend and backend service URLs

### 3. Repository Setup
- [ ] All code pushed to GitHub repository
- [ ] `render.yaml` file included in root directory
- [ ] All deployment files present

## Render Deployment Steps 🎯

### Method 1: Blueprint Deployment (Recommended)
1. [ ] Go to [Render Dashboard](https://dashboard.render.com)
2. [ ] Click "New" → "Blueprint"
3. [ ] Connect GitHub repository
4. [ ] Render automatically detects `render.yaml`
5. [ ] Configure environment variables:
   - Backend: `MONGO_URL`, `JWT_SECRET_KEY`
   - Frontend: `VITE_BACKEND_URL` (auto-configured)
6. [ ] Deploy services

### Method 2: Manual Deployment
#### Backend Service:
1. [ ] Create Web Service
2. [ ] Environment: Python 3
3. [ ] Build Command: `cd backend && pip install -r requirements.txt`
4. [ ] Start Command: `cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT`
5. [ ] Set environment variables
6. [ ] Deploy

#### Frontend Service:
1. [ ] Create Web Service
2. [ ] Environment: Node.js
3. [ ] Build Command: `cd frontend && yarn install && yarn build`
4. [ ] Start Command: `cd frontend && yarn preview --host 0.0.0.0 --port $PORT`
5. [ ] Set `VITE_BACKEND_URL` to backend service URL
6. [ ] Deploy

## Required Environment Variables 📋

### Backend (.env)
```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=Khelbhoomi
JWT_SECRET_KEY=your-secure-32-character-secret-key
CORS_ORIGINS=https://your-frontend-service.onrender.com
HOST=0.0.0.0
ENVIRONMENT=production
```

### Frontend (.env)
```env
VITE_BACKEND_URL=https://your-backend-service.onrender.com
NODE_ENV=production
```

## Post-Deployment Verification ✅

### 1. Backend Health Check
- [ ] Visit `https://your-backend-service.onrender.com/api/health`
- [ ] Should return: `{"status": "healthy"}`
- [ ] Check `/api/docs` (if not production) for API documentation

### 2. Database Connection
- [ ] Login with demo credentials works
- [ ] User registration creates new users
- [ ] Posts are loading correctly

### 3. Frontend Functionality
- [ ] Frontend loads successfully
- [ ] Demo login credentials display
- [ ] All pages navigate correctly (Home, Features, About, Messages)
- [ ] Login/logout functionality works
- [ ] User profiles display correctly

### 4. Authentication Flow
Test with demo users:
- [ ] `demo_athlete` / `demo123` (Athlete role)
- [ ] `demo_scout` / `demo123` (Scout role)
- [ ] `demo_fan` / `demo123` (Fan role)
- [ ] `testuser` / `password` (Test user)

### 5. API Integration
- [ ] Feed loads posts with images
- [ ] User profiles are accessible
- [ ] Edit profile functionality works
- [ ] Messages interface displays correctly

## Performance Optimization 🚀

### Free Tier Limitations
- [ ] Services may sleep after 15 minutes of inactivity
- [ ] 750 hours per month limit (shared across services)
- [ ] Consider upgrading to Starter plan for production

### Recommendations
- [ ] Upgrade to Starter plan ($7/month per service)
- [ ] Use MongoDB Atlas M10+ cluster for production
- [ ] Enable compression and caching
- [ ] Optimize build sizes

## Troubleshooting 🔧

### Common Issues
- [ ] **Build fails**: Check requirements.txt and package.json
- [ ] **Database connection error**: Verify MONGO_URL and IP whitelisting
- [ ] **CORS errors**: Update CORS_ORIGINS with frontend domain
- [ ] **JWT errors**: Ensure JWT_SECRET_KEY is set and secure
- [ ] **Frontend can't reach backend**: Verify VITE_BACKEND_URL

### Debugging Steps
- [ ] Check service logs in Render dashboard
- [ ] Verify environment variables are set correctly
- [ ] Test API endpoints individually
- [ ] Check MongoDB Atlas connection logs

## Security Checklist 🔒

- [ ] JWT secret key is secure (32+ characters)
- [ ] MongoDB Atlas IP whitelisting configured
- [ ] CORS origins restricted to frontend domain
- [ ] Production environment variables are secure
- [ ] No sensitive data in repository

## Monitoring & Maintenance 📊

- [ ] Set up Render service monitoring
- [ ] Monitor MongoDB Atlas usage
- [ ] Regular security updates
- [ ] Performance monitoring
- [ ] Error logging and reporting

---

## Quick Commands

### Test Local Build
```bash
# Backend
cd backend && uvicorn server:app --host 0.0.0.0 --port 8001

# Frontend  
cd frontend && yarn build && yarn preview --port 4173
```

### Generate JWT Secret
```bash
openssl rand -base64 32
# or
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Check Service Status
- Backend: `https://your-backend-service.onrender.com/api/health`
- Frontend: `https://your-frontend-service.onrender.com`

---

**🎉 Deployment Complete!** Your Khel Bhoomi sports platform is now live on Render.

For detailed instructions, see `RENDER_DEPLOYMENT_GUIDE.md`