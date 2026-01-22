# GitHub Pages Deployment Guide

## Prerequisites
- GitHub repository for your project
- Node.js and npm installed
- Backend deployed separately (e.g., Heroku, Railway, Render, or any cloud provider)

## Step 1: Update package.json

Add the homepage field to specify where the app will be hosted:

```json
{
  "name": "business-management-system-frontend",
  "version": "1.0.0",
  "homepage": "https://YOUR_USERNAME.github.io/YOUR_REPO_NAME",
  ...
}
```

Replace `YOUR_USERNAME` with your GitHub username and `YOUR_REPO_NAME` with your repository name.

## Step 2: Install GitHub Pages Deployment Package

```bash
cd frontend
npm install --save-dev gh-pages
```

## Step 3: Update Frontend API Configuration

Before building for production, update the API base URL to point to your deployed backend.

Create or update `frontend/.env.production`:

```
REACT_APP_API_URL=https://your-backend-url.com/api/v1
```

Replace `your-backend-url.com` with your actual backend URL (e.g., Heroku, Railway, etc.)

## Step 4: Build the Frontend

```bash
cd frontend
npm run build
```

This creates an optimized production build in the `build` folder.

## Step 5: Deploy to GitHub Pages

### Option A: Using gh-pages package (Recommended)

1. Add deployment scripts to `frontend/package.json`:

```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

2. Deploy:

```bash
cd frontend
npm run deploy
```

This will create a `gh-pages` branch and push your build folder to it.

### Option B: Manual Deployment

1. Build the app:
```bash
cd frontend
npm run build
```

2. Navigate to your GitHub repository → Settings → Pages

3. Source: Select "Deploy from a branch"

4. Branch: Select `gh-pages` and `/root` folder

5. Click Save

## Step 6: Configure GitHub Repository Settings

1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Under "Source", select branch `gh-pages` and folder `/ (root)`
4. Click **Save**
5. Your site will be published at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME`

## Step 7: Backend Deployment (Required)

Since GitHub Pages only hosts static files, you need to deploy your Flask backend separately.

### Backend Deployment Options:

#### A. Heroku (Free tier available)

1. Install Heroku CLI
2. Create `Procfile` in backend folder:
```
web: gunicorn run:app
```

3. Create `requirements.txt`:
```bash
cd backend
pip freeze > requirements.txt
```

4. Deploy:
```bash
heroku login
heroku create your-app-name
git subtree push --prefix backend heroku main
```

#### B. Railway.app (Recommended - Easy & Free)

1. Sign up at railway.app
2. Create new project
3. Connect GitHub repository
4. Set root directory to `backend`
5. Railway auto-detects Flask and deploys

#### C. Render.com (Free tier)

1. Sign up at render.com
2. Create new "Web Service"
3. Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn run:app`

#### D. PythonAnywhere (Free tier with limitations)

1. Sign up at pythonanywhere.com
2. Upload backend code
3. Configure WSGI file
4. Set up virtual environment

## Step 8: Update CORS Configuration

Update `backend/config.py` to allow your GitHub Pages domain:

```python
class Config:
    # ... existing config ...
    
    # Add your GitHub Pages URL to allowed origins
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:5000',
        'https://YOUR_USERNAME.github.io'
    ]
```

## Step 9: Test Deployment

1. Visit your GitHub Pages URL: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME`
2. Test login with: `admin` / `admin123`
3. Verify all features work correctly
4. Check browser console for any errors

## Troubleshooting

### Issue: Blank Page After Deployment

**Solution**: Check if homepage in package.json matches your GitHub Pages URL

### Issue: 404 on Refresh

**Solution**: Add a 404.html file in public folder that redirects to index.html:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Redirecting...</title>
    <script>
      sessionStorage.redirect = location.href;
    </script>
    <meta http-equiv="refresh" content="0;URL='/'">
  </head>
  <body>
  </body>
</html>
```

Add to `index.html` before closing `</body>`:

```html
<script>
  (function() {
    var redirect = sessionStorage.redirect;
    delete sessionStorage.redirect;
    if (redirect && redirect != location.href) {
      history.replaceState(null, null, redirect);
    }
  })();
</script>
```

### Issue: API Calls Failing

**Solution**: 
1. Check backend is running and accessible
2. Verify CORS is configured correctly
3. Check .env.production has correct API URL
4. Check browser console for CORS errors

### Issue: Images/Assets Not Loading

**Solution**: Use relative paths or PUBLIC_URL:

```javascript
// Instead of: src="/logo.png"
// Use:
src={process.env.PUBLIC_URL + '/logo.png'}
```

## Complete Deployment Checklist

- [ ] Backend deployed and accessible
- [ ] Backend CORS configured for GitHub Pages domain
- [ ] Frontend .env.production has correct backend URL
- [ ] package.json has correct homepage field
- [ ] gh-pages package installed
- [ ] Build succeeds without errors
- [ ] Deployed to GitHub Pages (npm run deploy)
- [ ] GitHub Pages settings configured
- [ ] Site accessible at GitHub Pages URL
- [ ] Login works correctly
- [ ] All features tested (Dashboard, Products, Sales, etc.)
- [ ] No console errors in production

## Automated Deployment with GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: |
        cd frontend
        npm install
    
    - name: Build
      run: |
        cd frontend
        npm run build
      env:
        REACT_APP_API_URL: ${{ secrets.API_URL }}
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./frontend/build
```

Add API_URL to repository secrets:
- Repository → Settings → Secrets → New repository secret
- Name: `API_URL`
- Value: `https://your-backend-url.com/api/v1`

## Maintenance

### Updating the Site

1. Make changes to your code
2. Commit and push to main branch
3. Run `npm run deploy` in frontend folder
4. Changes will be live in a few minutes

### Rolling Back

```bash
git checkout gh-pages
git log  # Find commit to revert to
git revert <commit-hash>
git push origin gh-pages
```

## Cost Summary

- **GitHub Pages**: FREE (with public repo)
- **Backend Options**:
  - Railway: FREE tier (500 hours/month)
  - Render: FREE tier (with limitations)
  - Heroku: FREE tier (deprecated, but paid plans available)
  - PythonAnywhere: FREE tier (limited)

## Support

If you encounter issues:
1. Check browser console for errors
2. Verify backend is accessible
3. Check GitHub Actions logs (if using)
4. Review GitHub Pages deployment status in repository settings

## Additional Resources

- [Create React App Deployment](https://create-react-app.dev/docs/deployment/#github-pages)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Flask Deployment Options](https://flask.palletsprojects.com/en/2.3.x/deploying/)
