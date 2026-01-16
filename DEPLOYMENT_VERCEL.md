# Vercel Deployment Guide for Giebee ERP

This guide walks you through deploying your Giebee ERP application to Vercel.

## Prerequisites

1.  **GitHub Account**: You need a GitHub account to host your code.
2.  **Vercel Account**: Sign up at [vercel.com](https://vercel.com) using your GitHub account.
3.  **Cloud Database**: Since Vercel is serverless, you cannot use the local SQLite file (`instance/database.db`). You need a hosted PostgreSQL database. We recommend **Neon** (easy to use) or **Vercel Storage** (Postgres).

## Step 1: Push Code to GitHub

(We have already pushed the code for you, but for future reference)
1.  Initialize git: `git init`
2.  Add files: `git add .`
3.  Commit: `git commit -m "Initial commit"`
4.  Create a repo on GitHub.
5.  Connect and push:
    ```bash
    git remote add origin <your-repo-url>
    git branch -M main
    git push -u origin main
    ```

## Step 2: Set up a Database

### Option A: Neon (Recommended for Free Tier)
1.  Go to [Neon.tech](https://neon.tech) and sign up.
2.  Create a new project.
3.  Copy the **Connection String** (it looks like `postgres://user:password@host/neondb...`).
4.  **Important**: You will use this as your `DATABASE_URL`.

### Option B: Vercel Postgres
1.  You can add a database directly during the Vercel project connection (see below).

## Step 3: Deploy on Vercel

1.  Go to your [Vercel Dashboard](https://vercel.com/dashboard).
2.  Click **"Add New..."** -> **"Project"**.
3.  Select your `GIEBEE_final` (or whatever you named it) repository and click **Import**.
4.  **Configure Project**:
    *   **Framework Preset**: Other (or Flask if it auto-detects, but "Other" is fine with our `vercel.json`).
    *   **Root Directory**: `./` (default).
    *   **Environment Variables**: You MUST set these.
        *   Expand the **Environment Variables** section.
        *   Add the following:
            *   `FLASK_SECRET_KEY`: (Enter a random long string for security)
            *   `DATABASE_URL`: (Paste your Postgres connection string from Step 2)
            *   `FLASK_ENV`: `production`

5.  Click **Deploy**.

## Step 4: Finalize Setup

1.  Wait for the deployment to finish.
2.  Once deployed, visit the URL provided by Vercel.
3.  The application should initialize the database tables automatically on the first run (thanks to `init_db()` in `main.py`).

## Troubleshooting

### "Internal Server Error"
*   Check the **Logs** tab in Vercel.
*   Most likely issue: Database connection failed. Verify `DATABASE_URL`.
*   Second most likely: Missing dependencies. Check `requirements.txt`.

### Database Tables Not Found
*   If tables aren't created, you might need to run a script or ensure `init_db()` is called. Our code calls `init_db()` on app startup, so it should work.

### Static Files (CSS/JS) Not Loading
*   Ensure `whitenoise` is configured correctly (it is already in `main.py`).
