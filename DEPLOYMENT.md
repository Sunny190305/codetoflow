# CodeToFlow Deployment Guide

## Deployment Options

I recommend **Render.com** for free deployment. It supports both frontend and backend.

## Option 1: Deploy to Render.com (Recommended - FREE)

### Prerequisites
- GitHub account
- Git installed on your computer

### Step 1: Prepare Your Code

1. **Initialize Git Repository** (if not already done):
```bash
cd c:\Users\ASUS\OneDrive\Desktop\Antigravity\CodeToFlow
git init
git add .
git commit -m "Initial commit"
```

2. **Create GitHub Repository**:
   - Go to [GitHub](https://github.com) and create a new repository named `codetoflow`
   - Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/codetoflow.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend on Render

1. Go to [Render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `codetoflow-backend`
   - **Root Directory**: `BackEnd`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`
5. Click **"Create Web Service"**
6. Wait for deployment (5-10 minutes)
7. **Copy your backend URL** (e.g., `https://codetoflow-backend.onrender.com`)

### Step 3: Deploy Frontend on Render

1. Click **"New +"** → **"Static Site"**
2. Connect the same GitHub repository
3. Configure:
   - **Name**: `codetoflow`
   - **Root Directory**: `FrontEnd`
   - **Build Command**: (leave empty)
   - **Publish Directory**: `.`
4. Click **"Create Static Site"**
5. Wait for deployment

### Step 4: Update Frontend to Use Production Backend

Update `FrontEnd/script.js` line 67:
```javascript
// Change from:
const response = await fetch("http://127.0.0.1:5000/parse", {

// To:
const response = await fetch("https://codetoflow-backend.onrender.com/parse", {
```

Commit and push:
```bash
git add .
git commit -m "Update API endpoint for production"
git push
```

Render will auto-deploy the changes!

### Your Live URLs:
- **Frontend**: `https://codetoflow.onrender.com`
- **Backend**: `https://codetoflow-backend.onrender.com`

---

## Option 2: Deploy to Vercel (Frontend) + Render (Backend)

### Backend on Render
Follow Step 2 above.

### Frontend on Vercel

1. Go to [Vercel.com](https://vercel.com) and sign up/login
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `FrontEnd`
   - **Build Command**: (leave empty)
   - **Output Directory**: `.`
5. Click **"Deploy"**
6. Update `script.js` with your Render backend URL

---

## Important Notes

⚠️ **Free Tier Limitations**:
- Render free tier spins down after 15 minutes of inactivity
- First request after inactivity may take 30-60 seconds
- Upgrade to paid tier ($7/month) for always-on service

✅ **What's Included**:
- All deployment config files are ready
- CORS is configured
- Production-ready setup

🔧 **Troubleshooting**:
- If backend fails, check Render logs
- Ensure `requirements.txt` has all dependencies
- Verify the backend URL in `script.js` is correct
