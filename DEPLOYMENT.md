# Deployment Guide - Academic Chatbot

## Railway Deployment

### Prerequisites
1. Railway account (https://railway.app)
2. GitHub repository connected to Railway
3. Required environment variables

### Required Environment Variables

Set these in Railway Dashboard → Variables:

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here
SESSION_SECRET=your_random_secret_key_here

# Optional - Firebase (uses mock database if not provided)
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
```

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Railway deployment configuration"
   git push
   ```

2. **Deploy on Railway**
   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect the configuration

3. **Verify Deployment**
   - Railway will use `railway.json` configuration
   - Gunicorn will start with optimal settings
   - Check logs for any errors

### Configuration Files

- **`application.py`** - Main Flask application with create_app() factory
- **`wsgi.py`** - WSGI entry point for production (imports from application.py)
- **`railway.json`** - Railway-specific configuration
- **`Procfile`** - Alternative deployment configuration
- **`gunicorn_config.py`** - Production server settings

### Important Note About File Structure

The project has:
- **`application.py`** (root level) - Contains the Flask app factory `create_app()`
- **`app/`** (directory) - Contains routes, services, templates, etc.

This naming convention avoids import conflicts in production environments.

### Troubleshooting

#### Error: "ModuleNotFoundError: No module named 'main'"
✅ **Fixed!** We've added `wsgi.py` as the proper entry point.

#### Port Issues
Railway automatically provides the `$PORT` environment variable. Our configuration uses it correctly.

#### Worker Crashes
The gunicorn config includes:
- Auto-restart on failure
- Worker recycling after 1000 requests
- 120-second timeout for long requests

### Local Testing with Production Config

Test the production setup locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=your_key
export SESSION_SECRET=your_secret
export PORT=8080

# Run with gunicorn (like production)
gunicorn wsgi:app --config gunicorn_config.py
```

### Performance Optimization

Current settings:
- **Workers**: 4 (auto-scales based on CPU)
- **Threads**: 2 per worker
- **Timeout**: 120 seconds
- **Keep-alive**: 5 seconds
- **Max requests**: 1000 (prevents memory leaks)

Adjust in `railway.json` or `gunicorn_config.py` as needed.

### Monitoring

Check Railway logs:
```
Railway Dashboard → Deployments → View Logs
```

Health check endpoint (add if needed):
```python
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

## Other Platforms

### Replit Deployment

Use Replit's built-in deployment:
1. Click "Deploy" button
2. Add environment variables
3. Replit handles the rest

### Heroku

Similar to Railway:
1. Add `Procfile` (already included)
2. Set environment variables
3. Push to Heroku

### Docker (Advanced)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]
```

---

**Need help?** Check the logs or contact support.
