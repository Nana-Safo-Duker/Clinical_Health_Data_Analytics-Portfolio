# Verify Streamlit Cloud Deployment
# Usage: .\VERIFY_DEPLOYMENT.ps1 -AppURL "https://your-app.streamlit.app/"

param(
    [Parameter(Mandatory=$true)]
    [string]$AppURL
)

Write-Host "`n=== VERIFYING STREAMLIT CLOUD DEPLOYMENT ===" -ForegroundColor Green
Write-Host "App URL: $AppURL`n" -ForegroundColor Cyan

try {
    # Test if the app is accessible
    Write-Host "Testing app accessibility..." -ForegroundColor Yellow
    
    $response = Invoke-WebRequest -Uri $AppURL -UseBasicParsing -ErrorAction Stop
    
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ App is LIVE and accessible!" -ForegroundColor Green
        Write-Host "   Status Code: $($response.StatusCode)" -ForegroundColor Green
        
        # Check if it's a Streamlit app
        if ($response.Content -match "streamlit" -or $response.Content -match "Streamlit") {
            Write-Host "✅ Confirmed: Streamlit app detected" -ForegroundColor Green
        }
        
        # Check for dashboard title
        if ($response.Content -match "Differential Gene Expression Dashboard") {
            Write-Host "✅ Dashboard title found" -ForegroundColor Green
        }
        
        Write-Host "`n=== DEPLOYMENT SUCCESSFUL ===" -ForegroundColor Green
        Write-Host "`nYour app is live at:" -ForegroundColor Cyan
        Write-Host "$AppURL" -ForegroundColor White
        Write-Host "`nNext steps:" -ForegroundColor Yellow
        Write-Host "1. Open the URL in your browser" -ForegroundColor White
        Write-Host "2. Test file upload functionality" -ForegroundColor White
        Write-Host "3. Verify visualizations work" -ForegroundColor White
        
    } else {
        Write-Host "⚠️  Unexpected status code: $($response.StatusCode)" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Error accessing app:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "`nPossible issues:" -ForegroundColor Yellow
    Write-Host "- App may still be deploying (wait 1-2 minutes)" -ForegroundColor White
    Write-Host "- URL may be incorrect" -ForegroundColor White
    Write-Host "- App may have deployment errors (check Streamlit Cloud logs)" -ForegroundColor White
}

Write-Host "`n"

