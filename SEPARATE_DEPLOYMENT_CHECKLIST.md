# 🚀 Khel Bhoomi - Separate Deployment Checklist

## Pre-Deployment Setup ✅

### MongoDB Atlas
- [ ] MongoDB Atlas account created
- [ ] Cluster created (M0 free tier)
- [ ] Database user created with read/write permissions
- [ ] IP whitelist: `0.0.0.0/0` (all IPs)
- [ ] Connection string obtained: `mongodb+srv://...`

### GitHub Repository  
- [ ] Code pushed to GitHub
- [ ] Repository connected to Render account

### Environment Configuration
- [ ] JWT secret key generated (32+ characters)
- [ ] Backend environment variables prepared
- [ ] Frontend environment updated with backend URL

## STEP 1: Backend Web Service 🐍

### Render Configuration
- [ ] Go to Render → "New" → "Web Service"
- [ ] Connect GitHub repository
- [ ] Service Name: `khel-bhoomi-backend`
- [ ] Environment: `Python 3`
- [ ] Root Directory: `backend`
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Environment Variables
Add these exact variables in Render dashboard:
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=Khelbhoomi  
JWT_SECRET_KEY=your-secure-32-character-secret-key
CORS_ORIGINS=*
HOST=0.0.0.0
ENVIRONMENT=production
```

### Backend Verification
- [ ] Service deploys successfully
- [ ] Health check works: `https://your-backend.onrender.com/api/health`
- [ ] API docs accessible (if not production): `/api/docs`
- [ ] Note backend URL for frontend configuration

## STEP 2: Frontend Static Site ⚛️

### Update Frontend Environment
Update `/app/frontend/.env`:
```env
VITE_BACKEND_URL=https://your-backend-service.onrender.com
NODE_ENV=production
```

### Render Configuration
- [ ] Go to Render → "New" → "Static Site"  
- [ ] Connect same GitHub repository
- [ ] Site Name: `khel-bhoomi-frontend`
- [ ] Root Directory: `frontend`
- [ ] Build Command: `yarn install && yarn build`
- [ ] Publish Directory: `dist`

### Frontend Verification
- [ ] Site builds successfully
- [ ] Frontend loads at your Render URL
- [ ] Demo login section displays
- [ ] Navigation works (Home, Features, About, Messages)
- [ ] Note frontend URL for CORS configuration

## STEP 3: Final Configuration 🔧

### Update Backend CORS
- [ ] Go to backend web service settings
- [ ] Update environment variable:
  ```
  CORS_ORIGINS=https://your-frontend-static-site.onrender.com
  ```
- [ ] Manual deploy backend to apply changes

### End-to-End Testing
Test with demo users:
- [ ] `demo_athlete` / `demo123` (Athlete)
- [ ] `demo_scout` / `demo123` (Scout)  
- [ ] `demo_fan` / `demo123` (Fan)
- [ ] `testuser` / `password` (Test user)

### Functionality Testing
- [ ] User login/logout works
- [ ] Feed loads with posts and images
- [ ] User profiles accessible
- [ ] Edit profile functionality works
- [ ] Messages interface displays
- [ ] Navigation between pages works

## Service URLs 📍

After deployment, you'll have:
- **Backend API**: `https://khel-bhoomi-backend.onrender.com`
- **Frontend App**: `https://khel-bhoomi-frontend.onrender.com`

## Quick Commands 💻

### Generate JWT Secret
```bash
openssl rand -base64 32
```

### Test Backend Health
```bash
curl https://your-backend.onrender.com/api/health
```

### Test Login
```bash
curl -X POST https://your-backend.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_athlete","password":"demo123"}'
```

## Troubleshooting 🔧

### Backend Issues
- [ ] Check build logs in Render dashboard
- [ ] Verify all environment variables are set
- [ ] Test MongoDB connection string locally
- [ ] Check service status and restart if needed

### Frontend Issues  
- [ ] Verify `VITE_BACKEND_URL` is correct
- [ ] Check browser console for errors
- [ ] Ensure backend CORS allows frontend domain
- [ ] Test build locally: `yarn build && npx serve dist`

### Common Solutions
- [ ] Restart both services if changes don't apply
- [ ] Check MongoDB Atlas user permissions
- [ ] Verify IP whitelist includes `0.0.0.0/0`
- [ ] Ensure environment variables have no extra spaces

## Cost Summary 💰

### Free Tier Usage
- **Backend Web Service**: 750 hours/month free
- **Frontend Static Site**: 100GB bandwidth free
- **MongoDB Atlas**: M0 cluster free

### Upgrade Options
- **Backend**: Starter plan $7/month for better performance
- **Frontend**: Pro plan $20/month for team features
- **Database**: M10 cluster $9/month for production

---

## 🎉 Deployment Complete!

Your Khel Bhoomi sports platform is now live with:
- ✅ Separate backend API service
- ✅ Separate frontend static site  
- ✅ Independent scaling and management
- ✅ Cost-effective deployment structure

**Frontend**: https://your-frontend.onrender.com  
**Backend**: https://your-backend.onrender.com

Users can now login with demo credentials and explore the full platform!