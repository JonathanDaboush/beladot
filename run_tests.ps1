# Clear Python caches
Write-Host "Clearing Python caches..."
Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Remove .pyc files
Get-ChildItem -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

# Remove pytest cache
if (Test-Path ".pytest_cache") {
    Remove-Item -Recurse -Force ".pytest_cache" -ErrorAction SilentlyContinue
}

Write-Host "Running backend tests..."
python -m pytest backend/tests/ -v --tb=short
