# Giebee Engineering ERP

This is a comprehensive ERP system for Giebee Engineering built with Flask and SQLAlchemy.

## Features

- **Dashboard**: Overview of key metrics and charts
- **Supplier Management**: Add and manage suppliers
- **Customer Management**: Add and manage customers
- **Inventory Management**: Track stock levels, add/remove inventory
- **quotation Management**: Create and manage quotations
- **Activity Management**: Track company activities
- **Financial Dashboard**: Revenue, expenses, and profit tracking
- **Fuel Tracking**: Monitor fuel consumption and costs
- **Mileage Tracking**: Track vehicle mileage and distances
- **Journey Tracking**: Monitor vehicle journeys and locations
- **Location Management**: Manage company locations
- **Pricing Management**: Set and manage service pricing

## Deployment Options

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the database:
   ```bash
   python -c "from database import init_db; init_db()"
   ```

3. Run the application:
   ```bash
   python main.py
   ```

### Production Deployment

#### Option 1: Render (Recommended - Free tier available)

1. Fork this repository on GitHub
2. Connect your GitHub account to Render
3. Create a new Web Service from your forked repository
4. Configure the following:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
5. Add environment variables:
   - `FLASK_SECRET_KEY`: Generate a secure random key
   - `DATABASE_URL`: PostgreSQL connection string (Render provides this automatically)
6. Deploy!

#### Option 2: Heroku (Step-by-Step Guide)

**Prerequisites:**
- Git installed
- Heroku CLI installed (download from https://devcenter.heroku.com/articles/heroku-cli)
- Heroku account (free tier available)

**Step 1: Prepare Your Application**
```bash
# Make sure you have all deployment files
# Procfile, runtime.txt, requirements.txt should be in your project root
ls -la
# Should show: Procfile, runtime.txt, requirements.txt, main.py, etc.
```

**Step 2: Initialize Git Repository (if not already done)**
```bash
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

**Step 3: Login to Heroku**
```bash
heroku login
# This will open your browser for authentication
```

**Step 4: Create Heroku App**
```bash
# Create app with a unique name (replace 'your-app-name' with your choice)
heroku create your-app-name

# Or let Heroku generate a name for you
heroku create
```

**Step 5: Add PostgreSQL Database**
```bash
# Add free PostgreSQL database
heroku addons:create heroku-postgresql:hobby-dev

# Verify the database was added
heroku addons
```

**Step 6: Set Environment Variables**
```bash
# Generate a secure secret key (you can use any random string)
heroku config:set FLASK_SECRET_KEY="your-very-secure-random-secret-key-here"

# Set debug to false for production
heroku config:set FLASK_DEBUG=false

# Check that DATABASE_URL is automatically set by PostgreSQL addon
heroku config
```

**Step 7: Deploy Your Application**
```bash
# Push your code to Heroku
git push heroku main

# If your branch is named 'master' instead of 'main':
git push heroku master
```

**Step 8: Initialize Database**
```bash
# Run database initialization command
heroku run python -c "from database import init_db; init_db()"
```

**Step 9: Open Your Application**
```bash
# Open the app in your browser
heroku open
```

**Step 10: Monitor and Troubleshoot**
```bash
# Check app logs
heroku logs --tail

# Check app status
heroku ps

# Restart app if needed
heroku restart
```

**Step 11: Scale Your App (Optional)**
```bash
# By default, Heroku runs 1 web dyno. You can scale if needed:
heroku ps:scale web=1
```

**Common Issues and Solutions:**

- **Build fails**: Check `heroku logs` for specific errors
- **Database connection fails**: Ensure PostgreSQL addon is attached and DATABASE_URL is set
- **Static files not loading**: WhiteNoise is configured to serve static files
- **App crashes**: Check logs with `heroku logs --tail`

**Cost:** Heroku offers a free tier with limitations. For production use, consider upgrading to paid dynos (~$7/month for basic plan).

#### Option 3: Railway

1. Connect your GitHub repository to Railway
2. Railway will automatically detect Python and install dependencies
3. Add PostgreSQL database from Railway dashboard
4. Set environment variables in Railway dashboard
5. Deploy!

## Database Configuration

The application supports multiple databases:

- **SQLite**: Default for local development (no setup required)
- **PostgreSQL**: Recommended for production (free tier available on Render, Railway, Supabase)
- **MySQL**: Alternative option

Set the `DATABASE_URL` environment variable to configure the database:

```bash
# SQLite (default)
DATABASE_URL=sqlite:///instance/database.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@host:port/database

# MySQL
DATABASE_URL=mysql+pymysql://user:password@host:port/database
```

## Environment Variables

- `FLASK_SECRET_KEY`: Secret key for Flask sessions (generate a secure random key)
- `DATABASE_URL`: Database connection string
- `FLASK_DEBUG`: Set to `false` for production

## Security Notes

- Change the default `FLASK_SECRET_KEY` in production
- Use HTTPS in production
- Regularly update dependencies
- Monitor database access logs
- Implement proper authentication if needed for production use
