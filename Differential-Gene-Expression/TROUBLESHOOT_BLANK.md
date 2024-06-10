# 🔧 Troubleshooting Blank Page Issue

## Problem
The Streamlit app is accessible (HTTP 200) but shows a blank page.

## Common Causes & Solutions

### 1. Check Streamlit Cloud Logs
**Action:** Go to Streamlit Cloud dashboard → Your app → "Logs"
- Look for Python errors
- Check import failures
- Verify package installation

### 2. Verify Main File Path
The main file path should be: `app/dashboard.py`
- Check in Streamlit Cloud settings
- Verify the path is correct

### 3. Check Requirements
All packages must be in `requirements.txt`:
- streamlit>=1.28.0
- pandas>=2.0.0
- numpy>=1.24.0
- altair>=5.0.0
- plotly>=5.17.0
- openpyxl>=3.1.0

### 4. Page Config Must Be First
`st.set_page_config()` must be the FIRST Streamlit command.

### 5. Browser Console Errors
Open browser developer tools (F12):
- Check Console tab for JavaScript errors
- Check Network tab for failed requests

## Quick Fix Steps

1. **Check Logs First** - Most important!
2. **Redeploy** - Sometimes fixes deployment issues
3. **Verify File Path** - Ensure `app/dashboard.py` is correct
4. **Clear Browser Cache** - Try incognito/private mode

