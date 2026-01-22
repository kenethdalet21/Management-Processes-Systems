# Quick Deployment Script for GitHub Pages

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  GitHub Pages Deployment Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if gh-pages is installed
Write-Host "[1/6] Checking dependencies..." -ForegroundColor Yellow
cd "D:\Management Processes Systems\frontend"

$packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
if (-not $packageJson.devDependencies.'gh-pages') {
    Write-Host "Installing gh-pages..." -ForegroundColor Green
    npm install --save-dev gh-pages
} else {
    Write-Host "✓ gh-pages already installed" -ForegroundColor Green
}

# Step 2: Check environment configuration
Write-Host ""
Write-Host "[2/6] Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env.production") {
    Write-Host "✓ .env.production found" -ForegroundColor Green
    $envContent = Get-Content ".env.production" -Raw
    if ($envContent -match "localhost") {
        Write-Host ""
        Write-Host "⚠ WARNING: .env.production still uses localhost!" -ForegroundColor Red
        Write-Host "Please update REACT_APP_API_URL with your deployed backend URL" -ForegroundColor Red
        Write-Host ""
        $continue = Read-Host "Continue anyway? (y/n)"
        if ($continue -ne 'y') {
            Write-Host "Deployment cancelled." -ForegroundColor Red
            exit
        }
    }
} else {
    Write-Host "✗ .env.production not found" -ForegroundColor Red
    Write-Host "Please create .env.production with your backend API URL" -ForegroundColor Red
    exit
}

# Step 3: Check package.json homepage
Write-Host ""
Write-Host "[3/6] Checking package.json homepage..." -ForegroundColor Yellow
if ($packageJson.homepage) {
    Write-Host "✓ Homepage set to: $($packageJson.homepage)" -ForegroundColor Green
} else {
    Write-Host "⚠ WARNING: 'homepage' not set in package.json" -ForegroundColor Yellow
    Write-Host "Please add: `"homepage`": `"https://YOUR_USERNAME.github.io/YOUR_REPO_NAME`"" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne 'y') {
        Write-Host "Deployment cancelled." -ForegroundColor Red
        exit
    }
}

# Step 4: Build the application
Write-Host ""
Write-Host "[4/6] Building production bundle..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Build failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "✓ Build successful" -ForegroundColor Green

# Step 5: Deploy to GitHub Pages
Write-Host ""
Write-Host "[5/6] Deploying to GitHub Pages..." -ForegroundColor Yellow
npm run deploy

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Deployment failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

# Step 6: Success message
Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "  ✓ Deployment Successful!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your site should be live in a few minutes at:" -ForegroundColor Cyan
if ($packageJson.homepage) {
    Write-Host $packageJson.homepage -ForegroundColor White
}
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to your GitHub repository" -ForegroundColor White
Write-Host "2. Settings → Pages" -ForegroundColor White
Write-Host "3. Verify source is set to 'gh-pages' branch" -ForegroundColor White
Write-Host "4. Wait a few minutes for deployment" -ForegroundColor White
Write-Host "5. Visit your site!" -ForegroundColor White
Write-Host ""
Write-Host "⚠ Don't forget to:" -ForegroundColor Yellow
Write-Host "- Deploy your backend to a cloud service" -ForegroundColor White
Write-Host "- Update .env.production with the backend URL" -ForegroundColor White
Write-Host "- Configure CORS on your backend" -ForegroundColor White
Write-Host ""
