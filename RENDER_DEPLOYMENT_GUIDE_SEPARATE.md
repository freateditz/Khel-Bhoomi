# Khel Bhoomi - Separate Web Service & Static Site Deployment

## Overview
Deploy Khel Bhoomi with:
- **Backend**: Web Service (FastAPI)  
- **Frontend**: Static Site (React build)

## Prerequisites

### 1. MongoDB Atlas Setup (Required)
- Create MongoDB Atlas account at https://www.mongodb.com/atlas
- Create cluster (M0 free tier available)
- Create database user with read/write permissions
- Whitelist all IP addresses: `0.0.0.0/0`
- Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/`

### 2. Render Account
- Create account at https://render.com
- Connect your GitHub repository

## Deployment Steps

### STEP 1: Deploy Backend as Web Service

1. **Create Web Service**
   - Go to Render Dashboard → "New" → "Web Service"
   - Connect your GitHub repository
   - **Root Directory**: `backend`

2. **Service Configuration**
   ```
   Name: khel-bhoomi-backend
   Environment: Python 3
   Region: Oregon (US West) or Singapore (Asia)
   Branch: main (or your main branch)
   Root Directory: backend
   
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn server:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables** (CRITICAL)
   Add these in the Environment section:
   ```
   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
   DB_NAME=Khelbhoomi
   JWT_SECRET_KEY=your-secure-32-character-secret-key-here
   CORS_ORIGINS=*
   HOST=0.0.0.0
   ENVIRONMENT=production
   ```

4. **Deploy Backend**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your backend URL: `https://khel-bhoomi-backend.onrender.com`

### STEP 2: Deploy Frontend as Static Site

1. **Update Frontend Environment**
   First, update `/app/frontend/.env` with your backend URL:
   ```env
   VITE_BACKEND_URL=https://your-backend-service-name.onrender.com
   NODE_ENV=production
   ```

2. **Create Static Site**
   - Go to Render Dashboard → "New" → "Static Site"
   - Connect your GitHub repository
   - **Root Directory**: `frontend`

3. **Static Site Configuration**
   ```
   Name: khel-bhoomi-frontend
   Branch: main (or your main branch)
   Root Directory: frontend
   
   Build Command: yarn install && yarn build
   Publish Directory: dist
   ```

4. **Deploy Frontend**
   - Click "Create Static Site"
   - Wait for build and deployment
   - Your frontend will be live at: `https://khel-bhoomi-frontend.onrender.com`

### STEP 3: Update CORS Configuration

1. **Update Backend CORS**
   After frontend deployment, update backend environment variable:
   ```
   CORS_ORIGINS=https://your-frontend-static-site.onrender.com
   ```

2. **Redeploy Backend**
   - Go to backend service in Render dashboard
   - Trigger manual deploy to apply CORS changes

## Required Environment Variables

### Backend Web Service (.env)
```env
# Database (REQUIRED)
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=Khelbhoomi

# Security (REQUIRED)
JWT_SECRET_KEY=generate-secure-32-character-key-here

# CORS (Update after frontend deployment)
CORS_ORIGINS=https://your-frontend-static-site.onrender.com

# Server Configuration
HOST=0.0.0.0
ENVIRONMENT=production
```

### Frontend Static Site (.env)
```env
# API Configuration (REQUIRED)
VITE_BACKEND_URL=https://your-backend-service.onrender.com

# Build Configuration
NODE_ENV=production
```

## Step-by-Step Checklist

### Backend Web Service ✅
- [ ] Create Web Service on Render
- [ ] Set Root Directory to `backend`
- [ ] Configure build/start commands
- [ ] Add all environment variables
- [ ] Deploy and verify health endpoint
- [ ] Test API endpoints work

### Frontend Static Site ✅  
- [ ] Update `.env` with backend URL
- [ ] Create Static Site on Render
- [ ] Set Root Directory to `frontend`
- [ ] Configure build command and publish directory
- [ ] Deploy and verify site loads
- [ ] Test login with demo credentials

### Final Configuration ✅
- [ ] Update CORS_ORIGINS with frontend URL
- [ ] Redeploy backend service
- [ ] Test full application flow
- [ ] Verify all features work end-to-end

## Commands for Manual Testing

### Generate JWT Secret
```bash
openssl rand -base64 32
# or
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Test Endpoints
```bash
# Health check
curl https://your-backend-service.onrender.com/api/health

# Login test
curl -X POST https://your-backend-service.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_athlete","password":"demo123"}'
```

### Local Build Test
```bash
# Backend
cd backend && uvicorn server:app --host 0.0.0.0 --port 8001

# Frontend
cd frontend && yarn build && npx serve dist -l 3000
```

## Demo Users for Testing
After deployment, test with these demo accounts:
- **Demo Athlete**: `demo_athlete` / `demo123`
- **Demo Scout**: `demo_scout` / `demo123`
- **Demo Fan**: `demo_fan` / `demo123`
- **Test User**: `testuser` / `password`

## Troubleshooting

### Backend Issues
- **Build fails**: Check `requirements.txt` completeness
- **Start fails**: Verify environment variables are set
- **Database errors**: Check MongoDB Atlas connection string and IP whitelist
- **CORS errors**: Ensure CORS_ORIGINS includes frontend URL

### Frontend Issues
- **Build fails**: Check `package.json` and dependencies
- **Blank page**: Check browser console for API connection errors
- **Login doesn't work**: Verify VITE_BACKEND_URL is correct
- **API errors**: Check backend CORS configuration

### Common Solutions
- Check service logs in Render dashboard
- Verify environment variables match exactly
- Ensure MongoDB Atlas user has proper permissions
- Test each service independently first

## Cost Information
- **Backend Web Service**: Free tier (750 hours/month) or Starter ($7/month)
- **Frontend Static Site**: Free tier (100GB bandwidth) or Pro ($20/month for team features)
- **Total Free Usage**: Both services can run on free tier with limitations

## Performance Tips
- Upgrade backend to Starter plan for better performance
- Use CDN for static assets (automatic with Render Static Sites)
- Optimize frontend bundle size
- Consider MongoDB Atlas M10+ for production

---

**🎉 Your Khel Bhoomi sports platform will be live with this deployment!**

Next: Follow the step-by-step checklist above to deploy both services.