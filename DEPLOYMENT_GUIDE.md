# Railway.app Deployment Guide for Giebee ERP

## Prerequisites
- GitHub account (free)
- Railway.app account (free tier available)

## Step-by-Step Deployment

### Step 1: Prepare Your Code for Deployment

#### Files to Upload to GitHub:
```
main.py                 # Main Flask application
database.py             # Database configuration
models.py               # SQLAlchemy models
migrate_db.py           # Database migration script
requirements.txt        # Python dependencies
pyproject.toml          # Project configuration
Procfile                # Railway process definition
runtime.txt             # Python version
README.md               # Project documentation

templates/              # HTML templates folder
static/                 # CSS, JS, images folder
```

#### Files to EXCLUDE:
```
instance/               # Local database files
__pycache__/            # Python cache
.vscode/                # VS Code settings
*.db                    # SQLite database files
uv.lock                 # Local dependency lock
.replit                 # Replit configuration
data/                   # Sample data (optional)
```

### Step 2: Create GitHub Repository

1. Go to https://github.com and sign in
2. Click "+" → "New repository"
3. Repository name: `giebee-erp` or `giebee-engineering-erp`
4. Make it Public or Private
5. **DO NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

### Step 3: Upload Files to GitHub

1. On your repository page, click "Upload files" or "uploading an existing file"
2. Drag and drop or select the files listed above
3. Add commit message: "Initial commit - Giebee ERP system"
4. Click "Commit changes"

### Step 4: Create Railway.app Account

1. Go to https://railway.app
2. Sign up with GitHub account (recommended)
3. Verify your email

### Step 5: Create Railway Project

1. Click "New Project"
2. Choose "Deploy from GitHub repo"
3. Connect your GitHub account to Railway
4. Select your `giebee-erp` repository
5. Click "Deploy"

### Step 6: Add PostgreSQL Database

1. In your Railway project dashboard, click "Add Database"
2. Select "PostgreSQL"
3. Choose database settings:
   - Name: giebee-db (or default)
   - Version: Latest (15+)
   - Region: Choose closest to your users
   - Plan: Free tier (512MB RAM, 1GB storage)
4. Click "Create Database"
5. Wait 1-2 minutes for provisioning

### Step 7: Configure Environment Variables

1. In your Railway project, go to "Variables" tab
2. Add these variables:

#### Required Variables:
```
DATABASE_URL=postgresql://[auto-generated-by-railway]
FLASK_APP=main.py
FLASK_ENV=production
FLASK_SECRET_KEY=your-secure-random-secret-key-here
SECRET_KEY=another-secure-random-key-for-sessions
```

#### How to get DATABASE_URL:
- Go to your PostgreSQL database in Railway
- Click "Connect" tab
- Copy the full DATABASE_URL

#### Generate Secure Keys:
Use a password generator or run this Python command:
```python
import secrets
print(secrets.token_hex(32))
```

### Step 8: Deploy and Test

1. Railway will automatically deploy when you add the database and variables
2. Monitor deployment logs in Railway dashboard
3. Once deployed, click "View site" to access your application
4. Test key functionality:
   - Dashboard loads
   - Database connection works
   - Can create/view invoices
   - Custom items work

### Step 9: Domain Setup (Optional)

1. In Railway project, go to "Settings" → "Domains"
2. Add custom domain or use Railway subdomain
3. Configure DNS if using custom domain

## Troubleshooting

### Common Issues:

1. **Database Connection Failed**:
   - Check DATABASE_URL format
   - Ensure PostgreSQL is fully provisioned
   - Verify environment variables are set

2. **Application Won't Start**:
   - Check Railway logs for error messages
   - Verify all required files are uploaded
   - Ensure Procfile is correct

3. **Import Errors**:
   - Check requirements.txt matches Railway's Python version
   - Verify all dependencies are listed

### Getting Help:
- Railway Documentation: https://docs.railway.app/
- Check Railway project logs
- Common Flask deployment issues

## Cost Structure

- **Free Tier**: 512MB RAM, 1GB disk, 100 hours/month
- **Hobby Plan**: $5/month (512MB RAM, 5GB disk, unlimited hours)
- **PostgreSQL**: Free tier available, paid plans start at $7/month

## Backup and Maintenance

- Railway provides automatic daily PostgreSQL backups
- Monitor usage in Railway dashboard
- Scale resources as needed

## Security Notes

- Never commit secrets to GitHub
- Use Railway's environment variables for sensitive data
- Keep dependencies updated
- Regularly backup your database
