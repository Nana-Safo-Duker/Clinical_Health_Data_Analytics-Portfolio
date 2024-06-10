# ✅ Post-Deployment Verification Guide

## 🎉 After Your App Deploys

Once Streamlit Cloud shows "Deployment successful", follow these steps:

---

## 🔗 Step 1: Get Your App URL

You'll see a URL like:
```
https://differential-gene-dashboard-xxxxx.streamlit.app/
```

**Copy this URL** - this is your live dashboard!

---

## 🧪 Step 2: Test Your Deployment

### Test 1: Basic Load Test
1. Open your app URL in a browser
2. ✅ Verify the page loads
3. ✅ Check the title: "🧬 Advanced Differential Gene Expression Dashboard"
4. ✅ Verify sidebar shows "📁 Data Upload"

### Test 2: Upload Sample Data
1. Click "Upload CSV file" in the sidebar
2. Upload: `data/examples/sample_data.csv`
   - If you don't have it locally, it's in the repository
3. ✅ Verify: "✅ File uploaded!" message appears

### Test 3: Column Mapping
After upload, you should see column selection:
1. ✅ Gene Name Column: Select `Gene`
2. ✅ Log2 Fold Change: Select `log2FoldChange`
3. ✅ Adjusted P-value: Select `padj`
4. ✅ Click anywhere to proceed

### Test 4: Visualizations
1. ✅ Check "Volcano Plot" tab loads
2. ✅ Adjust thresholds using sliders
3. ✅ Verify interactive charts work
4. ✅ Check other tabs (Top Genes, Distributions, etc.)

### Test 5: Export Functionality
1. Scroll to "💾 Export Results" section
2. ✅ Try downloading CSV
3. ✅ Try downloading Excel (if significant genes found)

---

## ✅ Success Checklist

- [ ] App loads without errors
- [ ] Can upload CSV file
- [ ] Column mapping works
- [ ] Visualizations render
- [ ] Threshold sliders work
- [ ] Export buttons work
- [ ] No console errors in browser

---

## 🐛 Troubleshooting

### Problem: App won't load
**Solution:**
- Check Streamlit Cloud logs
- Verify `app/dashboard.py` path is correct
- Check `requirements.txt` syntax

### Problem: Import errors
**Solution:**
- All packages in `requirements.txt`
- Check deployment logs for missing packages

### Problem: Visualizations not showing
**Solution:**
- Check browser console for errors
- Verify Plotly/Altair are installed
- Try refreshing the page

---

## 🔄 Updating Your App

To update the deployed app:

```bash
# Make your changes
git add .
git commit -m "Update dashboard"
git push origin main
```

Streamlit Cloud will **automatically redeploy** in 1-2 minutes!

---

## 📊 Your Live Dashboard

Once verified, your dashboard is ready to share:

- Share the URL with collaborators
- Bookmark it for easy access
- Use it for data analysis anytime!

---

## 🎯 Next Steps

1. ✅ Test all features
2. ✅ Share with team/researchers
3. ✅ Document any issues
4. ✅ Enjoy your live dashboard!

---

**Your Dashboard URL:** 
(Will be provided by Streamlit Cloud after deployment)

**Need help?** Check Streamlit Cloud logs or the repository issues.

