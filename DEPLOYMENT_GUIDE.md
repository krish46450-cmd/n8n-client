# Client App Deployment Guide

This guide will help you deploy the Windows Dump Analyzer Client App to Render.

## Prerequisites

- A [Render](https://render.com) account (free tier available)
- Git repository with your code (GitHub, GitLab, or Bitbucket)
- Google Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))
- Your Support Dashboard URL (if you've deployed it)

## Important Notes Before Deploying

### File Uploads & User Data

⚠️ **Important**: Render's free tier uses **ephemeral storage**. This means:
- Uploaded files (dump files, images, etc.) will be **deleted** when your service restarts or redeploys
- User uploads are stored in the `uploads/` folder which is **not persistent**

**Solutions**:
1. **For production**: Use external storage like AWS S3, Cloudinary, or Render Disks (paid)
2. **For demo/testing**: Accept that uploads will be temporary

### Windows-Specific Features

Some features won't work in production (Linux environment):
- **WinDbg analyzer**: Requires Windows - won't work on Render
- **Windows dump file locations**: Paths like `C:\Windows\Minidump` don't exist on Linux

These features will be **gracefully disabled** but won't crash the app.

## Deployment Steps

### Option 1: Automated Deployment (Recommended)

1. **Set up Git repository** (if not already done):
   ```bash
   cd Client_App
   git init
   git add .
   git commit -m "Prepare for deployment"
   ```

2. **Push to GitHub**:
   - Create a new repository on GitHub
   - Then run:
   ```bash
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

3. **Deploy on Render**:
   - Go to https://dashboard.render.com
   - Click "New" → "Blueprint"
   - Connect your Git repository
   - Select the repository
   - Render will detect `render.yaml` and create:
     - PostgreSQL database
     - Web service
   - **Before clicking "Apply"**, set these environment variables:

4. **Set Required Environment Variables** (in Render dashboard):

   Click on each environment variable that says "sync: false" and add the values:

   | Variable | Value | Required |
   |----------|-------|----------|
   | `GEMINI_API_KEY` | Your Google Gemini API key | **YES** |
   | `SUPPORT_API_URL` | Your Support Dashboard URL + `/api/tickets` | NO (if you deployed Support Dashboard) |
   | `SUPPORT_API_KEY` | Match the key from Support Dashboard | NO |
   | `MAIL_USERNAME` | Your Gmail address (for notifications) | NO |
   | `MAIL_PASSWORD` | Gmail App Password | NO |
   | `MAIL_DEFAULT_SENDER` | Email sender address | NO |

5. **Click "Apply"** to start deployment

6. **Wait for deployment** (3-5 minutes)

7. **Access your app** at the URL Render provides (e.g., `https://client-app-xxxxx.onrender.com`)

### Option 2: Manual Deployment

If you prefer to set up services manually:

#### Step 1: Create PostgreSQL Database

1. In Render Dashboard, click "New" → "PostgreSQL"
2. Configure:
   - Name: `client-db`
   - Database: `client_app`
   - User: `client_user`
   - Plan: Free
3. Click "Create Database"
4. Copy the "Internal Database URL"

#### Step 2: Create Web Service

1. Click "New" → "Web Service"
2. Connect your Git repository
3. Configure:
   - **Name**: `client-app`
   - **Root Directory**: `Client_App` (if repo root isn't the app)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

#### Step 3: Set Environment Variables

Add these in the web service settings:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `SECRET_KEY` | (generate random string - use password generator) |
| `FLASK_ENV` | `production` |
| `DATABASE_URL` | (paste PostgreSQL Internal Database URL) |
| `GEMINI_API_KEY` | (your Google Gemini API key) |
| `SUPPORT_API_URL` | (optional - your Support Dashboard URL + `/api/tickets`) |
| `SUPPORT_API_KEY` | (optional - match Support Dashboard key) |

#### Step 4: Deploy

1. Click "Create Web Service"
2. Wait for build and deployment to complete
3. Access your app at the provided URL

## Post-Deployment Configuration

### 1. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to Render environment variables
5. **Important**: Keep this key secret!

### 2. Connect Support Dashboard (Optional)

If you deployed the Support Dashboard:

1. Get your Support Dashboard URL from Render
2. Update Client App environment variables:
   - `SUPPORT_API_URL`: `https://support-dashboard-xxxxx.onrender.com/api/tickets`
   - `SUPPORT_API_KEY`: (same key you set in Support Dashboard)

3. Update Support Dashboard environment variables:
   - `CLIENT_API_URL`: `https://client-app-xxxxx.onrender.com/api`

### 3. Set Up Email Notifications (Optional)

For Gmail:
1. Enable 2-factor authentication on your Google account
2. Generate an [App Password](https://support.google.com/accounts/answer/185833)
3. Add to environment variables:
   - `MAIL_USERNAME`: your Gmail address
   - `MAIL_PASSWORD`: the App Password (not your regular password)
   - `MAIL_DEFAULT_SENDER`: `noreply@yourdomain.com`

### 4. Register Your First User

1. Visit your deployed app URL
2. Click "Register"
3. Create your admin account
4. Start using the app!

## Features & Limitations

### ✅ Working Features in Production

- User authentication and registration
- Support ticket system
- Chatbot with Google Gemini AI
- Image upload to chatbot
- Knowledge base management
- Email notifications
- CSV exports
- Dashboard analytics

### ⚠️ Limited Features

- **File Uploads**: Temporary storage only (deleted on restart)
  - Solution: Upgrade to Render Disk ($1/GB/month) or use AWS S3

- **WinDbg Integration**: Requires Windows
  - Won't work on Render (Linux servers)
  - Feature will be disabled gracefully

- **Windows Paths**: System paths like `C:\Windows\Minidump`
  - Not applicable on Linux
  - Features using these paths won't work

### 💡 Recommended Upgrades for Production

1. **Persistent Storage**:
   - Render Disk (starts at $1/GB/month)
   - AWS S3 integration for uploads

2. **Always-On Service**:
   - Upgrade to Starter plan ($7/month)
   - Prevents cold starts

3. **Database**:
   - Free tier: 1GB storage, shared CPU
   - Paid tier: $7/month (256MB RAM, 1GB storage, backups)

## Troubleshooting

### Build Fails

**Error**: `No module named 'google.genai'`
- Solution: Check that `google-genai` is in `requirements.txt`

**Error**: Database connection failed
- Solution: Verify `DATABASE_URL` is set correctly in environment variables

### App Won't Start

**Error**: `Address already in use`
- Solution: Render sets `PORT` automatically - don't hardcode port 5000

**Error**: `relation "users" does not exist`
- Solution: Database tables should auto-create. Check logs for initialization errors

### Features Not Working

**WinDbg/Dump Analyzer not working**:
- Expected on Linux servers - feature is Windows-only

**Uploads disappear after restart**:
- Expected on free tier - use persistent storage (S3, Render Disk)

**Gemini AI not responding**:
- Check `GEMINI_API_KEY` is set correctly
- Verify API key is valid at Google AI Studio
- Check API quota limits

### Cold Starts (Free Tier)

Free tier services spin down after 15 minutes of inactivity:
- First request takes 30-60 seconds
- Uploaded files are lost on spin-down
- Upgrade to Starter ($7/month) for always-on service

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Flask secret key for sessions | Yes | - |
| `FLASK_ENV` | Environment mode | Yes | `production` |
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `SUPPORT_API_URL` | Support Dashboard API endpoint | No | - |
| `SUPPORT_API_KEY` | API key for Support Dashboard | No | - |
| `MAIL_SERVER` | SMTP server | No | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | No | `587` |
| `MAIL_USE_TLS` | Use TLS for email | No | `true` |
| `MAIL_USERNAME` | Email username | No | - |
| `MAIL_PASSWORD` | Email password | No | - |
| `MAIL_DEFAULT_SENDER` | Default sender email | No | - |
| `PORT` | Port to run app (set by Render) | No | `5000` |

## Security Best Practices

1. **Never commit secrets** to Git
   - Use `.gitignore` to exclude `.env` files
   - Use Render environment variables for secrets

2. **Use strong secret keys**
   - Generate random strings for `SECRET_KEY`
   - Never use default values in production

3. **Protect API keys**
   - Keep Gemini API key secret
   - Rotate keys if exposed

4. **Email security**
   - Use Gmail App Passwords, not your main password
   - Enable 2FA on your Google account

5. **HTTPS only**
   - Render provides HTTPS automatically
   - Never disable HTTPS in production

## Cost Breakdown

**Free Tier** (Demo/Testing):
- PostgreSQL Database: Free (1GB storage)
- Web Service: Free (750 hours/month, cold starts)
- Storage: Ephemeral (temporary uploads)
- **Total**: $0/month

**Recommended Production Setup**:
- PostgreSQL: $7/month (always-on, backups)
- Web Service: $7/month (always-on, no cold starts)
- Render Disk (10GB): $10/month (persistent uploads)
- **Total**: $24/month

**Budget Option**:
- Web Service: $7/month (always-on)
- PostgreSQL: Free tier
- AWS S3: ~$0.50/month (for uploads)
- **Total**: ~$7.50/month

## Monitoring

### View Logs

1. Go to Render Dashboard
2. Click on your web service
3. Click "Logs" tab
4. Monitor real-time application logs

### Check Database

1. Go to your PostgreSQL database in Render
2. Click "Connect"
3. Use provided connection commands to access database

### Performance Monitoring

Free tier provides:
- Basic metrics (CPU, memory, requests)
- Log streaming
- Error notifications

## Next Steps

After successful deployment:

1. ✅ Test user registration and login
2. ✅ Test chatbot functionality
3. ✅ Create a support ticket
4. ✅ Test image uploads (remember they're temporary)
5. ✅ Configure email notifications
6. ✅ Connect Support Dashboard if deployed
7. ✅ Set up custom domain (optional)
8. ✅ Consider upgrading for production use

## Support Resources

- [Render Documentation](https://render.com/docs)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Last Updated**: January 2026
