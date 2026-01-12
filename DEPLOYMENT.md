# Deployment Guide

This guide covers multiple ways to host your stock prediction web application.

## Prerequisites

1. Make sure your app works locally:
   ```bash
   python app.py
   ```
   Then visit `http://localhost:5000` to test.

2. Create a GitHub repository (recommended for most hosting platforms):
   - Initialize git: `git init`
   - Add files: `git add .`
   - Commit: `git commit -m "Initial commit"`
   - Create repo on GitHub and push

---

## Option 1: Render (Recommended - Easy & Free)

**Best for**: Quick deployment with free tier

### Steps:

1. **Sign up** at [render.com](https://render.com) (free)

2. **Create a New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure**:
   - **Name**: `stock-prediction` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free

4. **Environment Variables** (if needed):
   - Usually not required for this app

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at `https://your-app-name.onrender.com`

**Note**: Free tier spins down after 15 minutes of inactivity. First request may take 30-60 seconds.

---

## Option 2: Railway (Easy & Fast)

**Best for**: Fast deployment with good free tier

### Steps:

1. **Sign up** at [railway.app](https://railway.app) (free with credit card)

2. **Deploy**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**:
   - Railway auto-detects Python
   - It will run `pip install -r requirements.txt` automatically
   - Start command: `python app.py`

4. **Deploy**:
   - Click "Deploy"
   - Your app will be live at `https://your-app-name.up.railway.app`

**Note**: Free tier includes $5 credit/month. Very fast deployments.

---

## Option 3: PythonAnywhere (Python-Focused)

**Best for**: Python developers, simple hosting

### Steps:

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com) (free tier available)

2. **Upload files**:
   - Go to "Files" tab
   - Upload all your project files

3. **Install dependencies**:
   - Go to "Tasks" tab
   - Create a new task: `pip3.10 install --user -r requirements.txt`
   - Run it

4. **Create Web App**:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Flask"
   - Select Python 3.10
   - Enter path to your `app.py`

5. **Configure**:
   - Set source code path
   - Set working directory
   - Reload web app

**Note**: Free tier has limitations but good for testing.

---

## Option 4: Fly.io (Good Free Tier)

**Best for**: Global deployment, good performance

### Steps:

1. **Install Fly CLI**:
   ```bash
   # Windows (PowerShell)
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Sign up**: `fly auth signup`

3. **Create app**:
   ```bash
   fly launch
   ```
   - Follow prompts
   - Don't deploy yet

4. **Create `fly.toml`** (I'll create this file)

5. **Deploy**:
   ```bash
   fly deploy
   ```

---

## Option 5: Heroku (Classic but Limited Free Tier)

**Best for**: If you already have Heroku account

### Steps:

1. **Install Heroku CLI**: [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login**:
   ```bash
   heroku login
   ```

3. **Create app**:
   ```bash
   heroku create your-app-name
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

**Note**: Heroku removed free tier, but has low-cost options.

---

## Option 6: Self-Hosted (VPS/Dedicated Server)

**Best for**: Full control, production use

### Using a VPS (DigitalOcean, Linode, AWS EC2):

1. **Get a VPS** (Ubuntu recommended)

2. **SSH into server**:
   ```bash
   ssh user@your-server-ip
   ```

3. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

4. **Clone your repo**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

5. **Set up virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Use Gunicorn** (better than Flask dev server):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

7. **Set up Nginx** as reverse proxy (for production)

8. **Use systemd** to keep it running

---

## Important Notes for Production

### 1. Use Gunicorn Instead of Flask Dev Server

Create `wsgi.py`:
```python
from app import app

if __name__ == "__main__":
    app.run()
```

Update `Procfile`:
```
web: gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 4
```

### 2. Environment Variables

For production, don't hardcode values. Use environment variables:
```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### 3. Update app.py for Production

The current `app.py` uses `debug=True` which is not secure for production.

---

## Quick Start: Render (Easiest)

1. Push code to GitHub
2. Sign up at render.com
3. Connect GitHub repo
4. Deploy
5. Done! 🎉

Your app will be live in ~10 minutes.

---

## Troubleshooting

- **Port issues**: Most platforms set `PORT` environment variable. Update `app.py` to use it.
- **Dependencies**: Make sure `requirements.txt` has all packages
- **Prophet installation**: Some platforms may need additional build tools
- **Memory**: Prophet can be memory-intensive. Consider upgrading if needed.

---

## Recommended for Beginners

**Start with Render** - it's the easiest and has a good free tier for testing.
