# 🚀 Deployment Guide - WanderWise Travel Recommender

## 📋 **API Keys Security**

**YES, you will need to upload your API keys**, but they will be stored securely as environment variables on the deployment platform. They will NOT be visible in your code.

## 🆓 **Free Deployment Options**

### **Option 1: Render (Recommended) - Easiest**

#### **Step 1: Prepare Your Repository**
1. Push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

#### **Step 2: Deploy on Render**
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `wanderwise-travel-recommender`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

#### **Step 3: Add Environment Variables**
In Render dashboard, go to your service → Environment:
- `OPENAI_API_KEY`: Your OpenAI API key
- `QLOO_API_KEY`: Your Qloo API key

#### **Step 4: Deploy**
Click "Create Web Service" - your app will be live in minutes!

---

### **Option 2: Railway - Fast & Reliable**

#### **Step 1: Deploy on Railway**
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect it's a Python app

#### **Step 2: Add Environment Variables**
In Railway dashboard → Variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `QLOO_API_KEY`: Your Qloo API key

#### **Step 3: Deploy**
Railway will automatically deploy your app!

---

### **Option 3: Heroku - Classic Choice**

#### **Step 1: Install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### **Step 2: Deploy**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

#### **Step 3: Add Environment Variables**
```bash
heroku config:set OPENAI_API_KEY=your_openai_key
heroku config:set QLOO_API_KEY=your_qloo_key
```

---

## 🔐 **API Keys Management**

### **How to Get API Keys:**

#### **OpenAI API Key:**
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up/Login
3. Go to "API Keys" section
4. Create new secret key
5. Copy the key (starts with `sk-`)

#### **Qloo API Key:**
1. Go to [qloo.com](https://qloo.com)
2. Sign up for the hackathon
3. Get your API key from the dashboard
4. Copy the key

### **Security Best Practices:**
- ✅ Store keys as environment variables
- ✅ Never commit keys to Git
- ✅ Use different keys for development/production
- ❌ Never hardcode keys in your code

---

## 🌐 **After Deployment**

### **Your App Will Be Available At:**
- **Render**: `https://your-app-name.onrender.com`
- **Railway**: `https://your-app-name.railway.app`
- **Heroku**: `https://your-app-name.herokuapp.com`

### **Test Your Deployment:**
1. Visit your app URL
2. Try getting recommendations for a location
3. Check the health endpoint: `your-url/health`

---

## 🛠️ **Troubleshooting**

### **Common Issues:**

#### **Build Fails:**
- Check if all dependencies are in `requirements.txt`
- Ensure Python version is compatible

#### **API Keys Not Working:**
- Verify keys are correctly set in environment variables
- Check if keys have proper permissions
- Ensure keys are not expired

#### **App Crashes:**
- Check logs in your deployment platform
- Ensure all environment variables are set
- Verify the start command is correct

---

## 📊 **Free Tier Limits**

### **Render:**
- 750 hours/month free
- Sleeps after 15 minutes of inactivity
- Auto-wakes on request

### **Railway:**
- $5 credit monthly
- Usually enough for small apps

### **Heroku:**
- Sleeps after 30 minutes
- Limited dyno hours
- Requires credit card for verification

---

## 🎯 **Recommendation**

**Use Render** - it's the easiest, most reliable, and has the best free tier for this type of application.

---

## 🚀 **Quick Deploy Checklist**

- [ ] Code pushed to GitHub
- [ ] API keys ready
- [ ] Chosen deployment platform
- [ ] Environment variables set
- [ ] App deployed successfully
- [ ] Tested the live app

**Happy Deploying! 🎉** 