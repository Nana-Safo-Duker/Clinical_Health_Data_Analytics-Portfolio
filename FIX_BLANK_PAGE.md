# 🔧 Fix Blank Page Issue - Step by Step

## 🔍 Immediate Actions

### Step 1: Check Streamlit Cloud Logs (MOST IMPORTANT!)

1. Go to **https://share.streamlit.io/**
2. Sign in to your account
3. Find your app: `differential-gene-expression-dashboard`
4. Click on it
5. Click **"Manage app"** or **"⚙️"** icon
6. Click **"Logs"** tab
7. **Look for:**
   - ❌ Python traceback errors
   - ❌ Import errors (missing packages)
   - ❌ FileNotFound errors
   - ⚠️ Warnings about missing files

**What to look for:**
```
Traceback (most recent call last):
  File "app/dashboard.py", line X...
```

---

### Step 2: Verify Main File Path

**In Streamlit Cloud settings:**
- Main file path should be: `app/dashboard.py`
- **NOT** `dashboard.py` or `./app/dashboard.py`

**To check/change:**
1. Go to your app in Streamlit Cloud
2. Click "⚙️ Settings"
3. Verify "Main file path" is `app/dashboard.py`
4. Save if changed

---

### Step 3: Test with Simple Version

Try deploying with the test file to isolate the issue:

**Change Main file path to:** `app/dashboard_simple.py`

This will help determine if it's:
- ✅ Imports issue → All imports fail
- ✅ Runtime issue → Main dashboard specific
- ✅ Path issue → Simple version also fails

---

### Step 4: Check Browser Console

1. Open your app URL
2. Press **F12** (or Right-click → Inspect)
3. Go to **Console** tab
4. Look for red error messages
5. Go to **Network** tab
6. Refresh page (F5)
7. Check for failed requests (red items)

---

## 🛠️ Common Fixes

### Fix 1: Add Error Handling
If logs show import errors, verify `requirements.txt` has all packages.

### Fix 2: Redeploy
Sometimes redeployment fixes issues:
1. Streamlit Cloud → Your app
2. Click "⚙️" → "Redeploy"
3. Wait for completion

### Fix 3: Clear Cache
1. Streamlit Cloud → Your app
2. Click "⚙️" → "Clear cache"
3. Redeploy

### Fix 4: Verify Repository
Ensure the repository has:
- ✅ `app/dashboard.py` exists
- ✅ `requirements.txt` exists
- ✅ All files are committed and pushed

---

## 📋 Diagnostic Checklist

- [ ] Checked Streamlit Cloud logs
- [ ] Verified main file path is `app/dashboard.py`
- [ ] All packages in requirements.txt
- [ ] No browser console errors
- [ ] Tried redeploying
- [ ] Cleared cache

---

## 🚨 Most Likely Causes

1. **Import Error** (60% likely)
   - Missing package in requirements.txt
   - Check logs for: `ModuleNotFoundError`

2. **Path Issue** (20% likely)
   - Wrong main file path
   - File doesn't exist at specified path

3. **Runtime Error** (15% likely)
   - Error in dashboard.py code
   - Check logs for traceback

4. **Browser Issue** (5% likely)
   - JavaScript errors
   - Cache issues

---

## 💡 Quick Test

Try changing main file to `app/dashboard_simple.py`:
- If this works → Issue is in main dashboard code
- If this also fails → Issue is with environment/packages

---

**Next Step:** Check the Streamlit Cloud logs first - that will tell us exactly what's wrong!

