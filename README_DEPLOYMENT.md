# 🚀 Khel Bhoomi - Render Deployment

## Quick Start

This sports platform is ready for **separate deployment** on Render:
- **Backend**: Web Service (FastAPI)
- **Frontend**: Static Site (React)

## Files Created

### Deployment Guides
- `RENDER_DEPLOYMENT_GUIDE_SEPARATE.md` - Complete step-by-step guide
- `SEPARATE_DEPLOYMENT_CHECKLIST.md` - Quick deployment checklist

### Configuration Files
- `backend/.env.webservice` - Backend environment template
- `frontend/.env.staticsite` - Frontend environment template

### Deployment Scripts
- `deploy-separate.sh` - Main deployment preparation script
- `backend/deploy-web-service.sh` - Backend-specific preparation
- `frontend/build-production.sh` - Frontend build script

## Quick Deploy

```bash
# 1. Run deployment preparation
./deploy-separate.sh

# 2. Push to GitHub
git add .
git commit -m "Ready for Render deployment"
git push origin main

# 3. Follow SEPARATE_DEPLOYMENT_CHECKLIST.md
```

## Requirements Before Deployment

### 1. MongoDB Atlas
- Create cluster at https://www.mongodb.com/atlas
- Get connection string
- Whitelist all IPs: `0.0.0.0/0`

### 2. Environment Variables
**Backend Web Service:**
```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=Khelbhoomi
JWT_SECRET_KEY=secure-32-character-secret-key
CORS_ORIGINS=https://your-frontend.onrender.com
HOST=0.0.0.0
ENVIRONMENT=production
```

**Frontend Static Site:**
```env
VITE_BACKEND_URL=https://your-backend.onrender.com
NODE_ENV=production
```

## Render Configuration

### Backend Web Service
```
Name: khel-bhoomi-backend
Environment: Python 3
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn server:app --host 0.0.0.0 --port $PORT
```

### Frontend Static Site  
```
Name: khel-bhoomi-frontend
Root Directory: frontend
Build Command: yarn install && yarn build
Publish Directory: dist
```

## Demo Users

After deployment, test with these accounts:
- **Demo Athlete**: `demo_athlete` / `demo123`
- **Demo Scout**: `demo_scout` / `demo123`
- **Demo Fan**: `demo_fan` / `demo123`
- **Test User**: `testuser` / `password`

## Features Included

- ✅ User authentication with JWT
- ✅ Role-based access (Athlete, Scout, Fan)
- ✅ User profiles with edit functionality
- ✅ Social feed with posts and images
- ✅ Sports-specific content and tagging
- ✅ Messages interface
- ✅ Responsive design
- ✅ MongoDB Atlas integration
- ✅ Production-ready configuration

## Support

For deployment issues:
1. Check service logs in Render dashboard
2. Verify environment variables are set correctly
3. Test MongoDB Atlas connection
4. Ensure CORS configuration includes frontend domain

## Cost

**Free Tier:**
- Backend Web Service: 750 hours/month
- Frontend Static Site: 100GB bandwidth
- MongoDB Atlas: M0 cluster

**Production:**
- Backend: $7/month (Starter plan)
- Frontend: Free or $20/month (Pro features)
- Database: $9/month (M10 cluster)

---

**🎉 Your Khel Bhoomi sports platform is ready for Render deployment!**

Follow `SEPARATE_DEPLOYMENT_CHECKLIST.md` for step-by-step instructions.