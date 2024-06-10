# 🚀 Quick Deploy to Streamlit Cloud - Step by Step

## ✅ Pre-Deployment Checklist

All required files are verified:
- ✅ `app/dashboard.py` - Main dashboard file
- ✅ `requirements.txt` - All dependencies listed
- ✅ `streamlit_app.py` - Entry point (optional)
- ✅ Repository pushed to GitHub

## 📋 Deployment Steps (5 minutes)

### Step 1: Go to Streamlit Cloud
Open in your browser:
**https://share.streamlit.io/**

### Step 2: Sign In
- Click **"Sign in"** button (top right)
- Choose **"Sign in with GitHub"**
- Authorize Streamlit Cloud access

### Step 3: Create New App
- Click **"New app"** button
- You'll see the deployment form

### Step 4: Configure Your App

Fill in these details:

**Repository:**
```
Nana-Safo-Duker/Differential-Gene-Expression-Dashboard
```
(Or use: `Nana-Safo-Duker/Differential-Gene-Expression`)

**Branch:**
```
main
```

**Main file path:**
```
app/dashboard.py
```
(Alternative: `streamlit_app.py`)

**App URL (optional):**
```
differential-gene-dashboard
```
(This will create: `https://differential-gene-dashboard.streamlit.app/`)

### Step 5: Deploy!
- Click the **"Deploy!"** button
- Wait 1-2 minutes for deployment
- Watch the build logs

### Step 6: Access Your App
Once deployed, you'll get a URL like:
```
https://differential-gene-dashboard-xxxxx.streamlit.app/
```

## 🎯 Repository Options

You have two repositories ready:

### Option 1: Dashboard Repository (Recommended)
- **Repository:** `Nana-Safo-Duker/Differential-Gene-Expression-Dashboard`
- **URL:** https://github.com/Nana-Safo-Duker/Differential-Gene-Expression-Dashboard
- **Main file:** `app/dashboard.py`
- **Why:** Dedicated dashboard repository

### Option 2: Main Repository
- **Repository:** `Nana-Safo-Duker/Differential-Gene-Expression`
- **URL:** https://github.com/Nana-Safo-Duker/Differential-Gene-Expression
- **Main file:** `app/dashboard.py`
- **Why:** Full project repository

Both will work perfectly!

## 🔍 Verification

After deployment, verify:
1. ✅ App loads without errors
2. ✅ Can upload sample data (`data/examples/sample_data.csv`)
3. ✅ Visualizations render correctly
4. ✅ Export functionality works

## 📊 Testing Your Deployment

Once live, test with:
1. Upload sample data: `data/examples/sample_data.csv`
2. Map columns:
   - Gene: `Gene`
   - Log2FC: `log2FoldChange`
   - P-adjusted: `padj`
3. Adjust thresholds
4. Explore visualizations
5. Export results

## 🔄 Auto-Deployment

Once connected, every push to `main` branch automatically redeploys:
```bash
git push origin main
# Streamlit Cloud auto-deploys in ~1-2 minutes
```

## ⚠️ Troubleshooting

**Problem:** Build fails
- ✅ Check `requirements.txt` syntax
- ✅ Verify main file path is correct
- ✅ Check Streamlit Cloud logs

**Problem:** Import errors
- ✅ All dependencies in `requirements.txt`
- ✅ File paths are correct

**Problem:** App won't load
- ✅ Check GitHub repository is public
- ✅ Verify main file exists at specified path

## 📞 Need Help?

- **Streamlit Docs:** https://docs.streamlit.io/
- **Streamlit Cloud:** https://docs.streamlit.io/streamlit-community-cloud
- **Your Repo:** https://github.com/Nana-Safo-Duker/Differential-Gene-Expression-Dashboard

## 🎉 Success!

Once deployed, share your app URL:
```
https://[your-app-name].streamlit.app/
```

---

**Ready to deploy?** Go to: https://share.streamlit.io/ 🚀

