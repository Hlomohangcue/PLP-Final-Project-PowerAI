# PowerAI Cleanup Script
# This script removes old Flask files and test files that are no longer needed
# Run this ONLY after backing up your project!

Write-Host "PowerAI Project Cleanup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will remove old Flask files and test files." -ForegroundColor Yellow
Write-Host "Make sure you have a backup before proceeding!" -ForegroundColor Red
Write-Host ""

$response = Read-Host "Do you want to continue? (yes/no)"
if ($response -ne "yes") {
    Write-Host "Cleanup cancelled." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Starting cleanup..." -ForegroundColor Green

# Files to remove
$filesToRemove = @(
    "powerai_app.py",
    "powerai_simple.py",
    "comprehensive_dashboard.py",
    "advanced_api_system.py",
    "enhanced_dashboard.py",
    "company_analytics.py",
    "company_registration.py",
    "mysql_config.py",
    "real_data_config.py",
    "real_data_integration.py",
    "weather_service.py",
    "weather_demo.py",
    "setup_mysql_database.py",
    "setup_real_data.py",
    "setup_weather_api.py",
    "test_company_specific_analytics.py",
    "test_flask_integration.py",
    "test_mysql_integration.py",
    "test_mysql_simple.py",
    "test_powerai_enhanced.py",
    "test_pretrained_integration.py",
    "test_routes.py",
    "verify_company_analytics.py",
    "verify_models.py",
    "powerai.log",
    "powerai_simple.log",
    "powerai_real_data.db",
    "pending_registrations.json",
    "sarimax_forecast.csv",
    "model_metadata.json",
    "requirements.txt",
    "DASHBOARD_REGISTRATION_FIXES_COMPLETE.md",
    "MYSQL_INTEGRATION_SUMMARY.md",
    "ROUTE_FIXES_COMPLETE.md",
    "REAL_DATA_INTEGRATION_GUIDE.md",
    "PRETRAINED_MODELS_GUIDE.md"
)

# Directories to remove
$dirsToRemove = @(
    "templates",
    "config",
    "notebooks",
    "__pycache__"
)

# Remove files
Write-Host ""
Write-Host "Removing files..." -ForegroundColor Yellow
foreach ($file in $filesToRemove) {
    $filePath = Join-Path $PSScriptRoot $file
    if (Test-Path $filePath) {
        Remove-Item $filePath -Force
        Write-Host "  ✓ Removed: $file" -ForegroundColor Green
    } else {
        Write-Host "  - Not found: $file" -ForegroundColor Gray
    }
}

# Remove directories
Write-Host ""
Write-Host "Removing directories..." -ForegroundColor Yellow
foreach ($dir in $dirsToRemove) {
    $dirPath = Join-Path $PSScriptRoot $dir
    if (Test-Path $dirPath) {
        Remove-Item $dirPath -Recurse -Force
        Write-Host "  ✓ Removed: $dir/" -ForegroundColor Green
    } else {
        Write-Host "  - Not found: $dir/" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Cleanup completed!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Remaining files (core Streamlit application):" -ForegroundColor Cyan
Write-Host "  ✓ streamlit_app.py" -ForegroundColor Green
Write-Host "  ✓ config_multi_tenant.py" -ForegroundColor Green
Write-Host "  ✓ pretrained_models.py" -ForegroundColor Green
Write-Host "  ✓ enhanced_demand_forecasting.py" -ForegroundColor Green
Write-Host "  ✓ requirements-streamlit.txt" -ForegroundColor Green
Write-Host "  ✓ models/ (directory)" -ForegroundColor Green
Write-Host "  ✓ DOCUMENTATION.md" -ForegroundColor Green
Write-Host "  ✓ DEPLOYMENT.md" -ForegroundColor Green
Write-Host "  ✓ README.md" -ForegroundColor Green
Write-Host "  ✓ PROJECT_SUMMARY.md" -ForegroundColor Green
Write-Host "  ✓ Dockerfile" -ForegroundColor Green
Write-Host "  ✓ docker-compose.yml" -ForegroundColor Green
Write-Host "  ✓ .streamlit/config.toml" -ForegroundColor Green
Write-Host "  ✓ .gitignore" -ForegroundColor Green
Write-Host ""
Write-Host "Your project is now clean and ready for submission!" -ForegroundColor Cyan
