# 🚀 Streamlit Cloud Deployment Guide

Deploy your Differential Gene Expression Dashboard to Streamlit Cloud for free!

## 📋 Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Streamlit Cloud Account** - Sign up at https://share.streamlit.io/
3. **Repository URL** - The GitHub repository with your dashboard code

## 🎯 Quick Deployment Steps

### Step 1: Prepare Your Repository

✅ Make sure these files exist in your repository:
- `app/dashboard.py` - Main dashboard application
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration (optional)

### Step 2: Connect to Streamlit Cloud

1. Go to **https://share.streamlit.io/**
2. Click **"Sign in with GitHub"**
3. Authorize Streamlit Cloud to access your repositories

### Step 3: Deploy Your App

1. Click **"New app"**
2. Select your repository: `Nana-Safo-Duker/Differential-Gene-Expression-Dashboard`
3. Set **Main file path** to one of:
   - `app/dashboard.py` (recommended)
   - `streamlit_app.py` (alternative entry point)
4. Set **App URL** (optional - auto-generated if left blank)
   - Example: `differential-gene-expression-dashboard`
5. Click **"Deploy!"**

### Step 4: Access Your Live App

- Streamlit Cloud will generate a URL like:
  - `https://differential-gene-expression-dashboard-xxxxx.streamlit.app/`
- Your app will be live in 1-2 minutes
- Updates automatically deploy when you push to the main branch

## 📁 Required Files

### requirements.txt (Already exists)
```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
altair>=5.0.0
plotly>=5.17.0
openpyxl>=3.1.0
```

### .streamlit/config.toml (Optional, but recommended)
Already created in your repository for optimal configuration.

## ⚙️ Configuration Options

### Main File Path Options:

**Option 1: Direct Dashboard** (Recommended)
```
app/dashboard.py
```

**Option 2: Entry Point**
```
streamlit_app.py
```

### Advanced Settings:

- **Python version:** Default (3.9+) works fine
- **Branch:** `main` (default)
- **Always rerun:** Enable for auto-refresh on updates

## 🔄 Updating Your App

Your app auto-updates when you push to the connected branch:

```bash
git add .
git commit -m "Update dashboard features"
git push origin main
```

Streamlit Cloud will automatically rebuild and redeploy (~1-2 minutes).

## 🐛 Troubleshooting

### Common Issues:

**1. Import Errors**
- Ensure `requirements.txt` includes all dependencies
- Check that file paths are correct

**2. App Not Loading**
- Check Streamlit Cloud logs for errors
- Verify `requirements.txt` syntax is correct
- Ensure main file path is correct

**3. Slow Performance**
- Streamlit Cloud free tier has resource limits
- Consider upgrading for production use

### Check Logs:
- Go to your app in Streamlit Cloud
- Click "Manage app" → "Logs"
- Review error messages

## 📊 App Configuration

Your dashboard includes:
- ✅ Interactive volcano plots
- ✅ Data upload and processing
- ✅ Export functionality
- ✅ Multiple visualization types
- ✅ Sample data for testing

## 🔗 Useful Links

- **Streamlit Cloud:** https://share.streamlit.io/
- **Documentation:** https://docs.streamlit.io/
- **Your Repository:** https://github.com/Nana-Safo-Duker/Differential-Gene-Expression-Dashboard

## 🎉 Success!

Once deployed, your dashboard will be accessible at:
```
https://[your-app-name].streamlit.app/
```

Share this URL with collaborators, researchers, or anyone who needs to analyze gene expression data!

---

**Note:** Streamlit Cloud free tier includes:
- Unlimited public apps
- Automatic HTTPS
- Auto-deployment from GitHub
- Community support

For private apps or higher resource limits, consider upgrading to Streamlit Cloud for Teams.

