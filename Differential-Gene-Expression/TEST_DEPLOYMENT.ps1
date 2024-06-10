# Test Deployment Script
# This script helps verify your Streamlit Cloud deployment

Write-Host "`n=== STREAMLIT CLOUD DEPLOYMENT TEST ===" -ForegroundColor Green
Write-Host "`nTesting deployment readiness..." -ForegroundColor Yellow

# Check required files
$files = @(
    "app/dashboard.py",
    "requirements.txt",
    "streamlit_app.py"
)

Write-Host "`nChecking required files..." -ForegroundColor Cyan
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file - MISSING" -ForegroundColor Red
    }
}

# Check requirements.txt content
Write-Host "`nChecking requirements.txt..." -ForegroundColor Cyan
if (Test-Path "requirements.txt") {
    $requirements = Get-Content "requirements.txt"
    $required = @("streamlit", "pandas", "numpy", "plotly", "altair", "openpyxl")
    
    foreach ($req in $required) {
        $found = $requirements | Select-String -Pattern $req
        if ($found) {
            Write-Host "  ✅ $req" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  $req - Not found" -ForegroundColor Yellow
        }
    }
}

# Check git status
Write-Host "`nChecking git status..." -ForegroundColor Cyan
$gitStatus = git status --short
if ($gitStatus) {
    Write-Host "  ⚠️  Uncommitted changes detected" -ForegroundColor Yellow
    Write-Host "  Consider committing before deployment" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ Working tree clean" -ForegroundColor Green
}

# Check remote
Write-Host "`nChecking remote repository..." -ForegroundColor Cyan
$remote = git remote get-url dashboard 2>$null
if ($remote) {
    Write-Host "  ✅ Dashboard remote: $remote" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Dashboard remote not configured" -ForegroundColor Yellow
}

Write-Host "`n=== DEPLOYMENT READY ===" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://share.streamlit.io/" -ForegroundColor White
Write-Host "2. Click 'New app'" -ForegroundColor White
Write-Host "3. Use these settings:" -ForegroundColor White
Write-Host "   Repository: Nana-Safo-Duker/Differential-Gene-Expression-Dashboard" -ForegroundColor White
Write-Host "   Branch: main" -ForegroundColor White
Write-Host "   Main file: app/dashboard.py" -ForegroundColor White
Write-Host "4. Click 'Deploy!'" -ForegroundColor White
Write-Host "`n" -ForegroundColor White

