# Production Deployment Guide

## Deployment Options

### Option 1: Cloud Deployment (Azure/AWS/GCP)

#### Backend Deployment

1. **Prepare the application**
   ```bash
   cd backend
   pip freeze > requirements.txt
   ```

2. **Set environment variables**
   - `SECRET_KEY`: Strong random key
   - `JWT_SECRET_KEY`: Strong random key
   - `DATABASE_URL`: Production database URL
   - `FLASK_ENV`: production

3. **Deploy to Azure App Service**
   ```bash
   # Install Azure CLI
   # Login
   az login
   
   # Create resource group
   az group create --name bms-rg --location eastus
   
   # Create App Service plan
   az appservice plan create --name bms-plan --resource-group bms-rg --sku B1 --is-linux
   
   # Create web app
   az webapp create --resource-group bms-rg --plan bms-plan --name bms-api --runtime "PYTHON:3.11"
   
   # Configure environment variables
   az webapp config appsettings set --resource-group bms-rg --name bms-api --settings \
     SECRET_KEY="your-secret-key" \
     JWT_SECRET_KEY="your-jwt-key" \
     DATABASE_URL="postgresql://..." \
     FLASK_ENV="production"
   
   # Deploy
   az webapp up --name bms-api --resource-group bms-rg
   ```

#### Frontend Deployment

1. **Build the application**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Azure Static Web Apps or CDN**
   ```bash
   # Option 1: Azure Static Web Apps
   az staticwebapp create \
     --name bms-frontend \
     --resource-group bms-rg \
     --source ./build \
     --location eastus
   
   # Option 2: Deploy to Azure Blob Storage + CDN
   az storage account create --name bmsstorage --resource-group bms-rg
   az storage blob service-properties update --account-name bmsstorage --static-website --index-document index.html
   az storage blob upload-batch --account-name bmsstorage --destination '$web' --source ./build
   ```

### Option 2: Docker Deployment

#### Create Docker Files

**Backend Dockerfile** (`backend/Dockerfile`):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

**Frontend Dockerfile** (`frontend/Dockerfile`):
```dockerfile
FROM node:18 as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml** (root directory):
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: business_management_system
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/business_management_system
      SECRET_KEY: your-secret-key
      JWT_SECRET_KEY: your-jwt-key
      FLASK_ENV: production
    depends_on:
      - postgres
    ports:
      - "5000:5000"

  frontend:
    build: ./frontend
    depends_on:
      - backend
    ports:
      - "80:80"

volumes:
  postgres_data:
```

**Deploy with Docker Compose:**
```bash
docker-compose up -d
```

### Option 3: Desktop Application (Electron)

1. **Install Electron dependencies**
   ```bash
   cd frontend
   npm install electron electron-builder --save-dev
   ```

2. **Create Electron main file** (`frontend/public/electron.js`)

3. **Add build script to package.json**
   ```json
   "build:desktop": "react-scripts build && electron-builder"
   ```

4. **Build desktop app**
   ```bash
   npm run build:desktop
   ```

## Database Migration

### PostgreSQL Production Setup

1. **Create production database**
   ```bash
   psql -U postgres
   CREATE DATABASE business_management_system_prod;
   CREATE USER bms_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE business_management_system_prod TO bms_user;
   ```

2. **Configure backup**
   ```bash
   # Create backup script
   pg_dump -U postgres business_management_system_prod > backup_$(date +%Y%m%d).sql
   
   # Schedule daily backups (cron)
   0 2 * * * /path/to/backup-script.sh
   ```

3. **Restore from backup**
   ```bash
   psql -U postgres business_management_system_prod < backup.sql
   ```

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Enable database encryption
- [ ] Regular security updates
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Enable database backups
- [ ] Use environment variables for secrets
- [ ] Implement proper error handling

## Performance Optimization

1. **Backend**
   - Use connection pooling
   - Enable database indexing
   - Implement caching (Redis)
   - Use gunicorn with multiple workers
   - Enable compression

2. **Frontend**
   - Enable production build
   - Use CDN for static assets
   - Implement lazy loading
   - Enable browser caching
   - Minify assets

## Monitoring

1. **Application Monitoring**
   - Set up application logs
   - Monitor API response times
   - Track error rates
   - Monitor resource usage

2. **Database Monitoring**
   - Monitor query performance
   - Track connection pool usage
   - Monitor storage usage
   - Set up alerts for slow queries

## Scaling

1. **Horizontal Scaling**
   - Use load balancer
   - Deploy multiple backend instances
   - Use managed database service

2. **Vertical Scaling**
   - Increase server resources
   - Optimize database configuration
   - Implement caching layer

## Maintenance

1. **Regular Updates**
   ```bash
   # Update dependencies
   pip install --upgrade -r requirements.txt
   npm update
   ```

2. **Database Maintenance**
   ```bash
   # Vacuum database
   psql -U postgres -d business_management_system -c "VACUUM ANALYZE;"
   
   # Check database size
   psql -U postgres -c "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) FROM pg_database;"
   ```

## Support and Troubleshooting

For production issues:
1. Check application logs
2. Check database logs
3. Verify environment variables
4. Check network connectivity
5. Monitor resource usage

## Rollback Procedure

1. **Restore previous version**
   ```bash
   # Restore from backup
   psql -U postgres business_management_system < backup_previous.sql
   
   # Redeploy previous version
   git checkout <previous-tag>
   # Follow deployment steps
   ```

## Disaster Recovery

1. **Regular Backups**
   - Daily database backups
   - Weekly full system backups
   - Store backups in multiple locations

2. **Recovery Plan**
   - Document recovery procedures
   - Test recovery process regularly
   - Maintain backup of environment configuration

---

For additional support, refer to the main README.md or contact the development team.
