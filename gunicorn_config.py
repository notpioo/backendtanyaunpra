"""
Gunicorn configuration for production deployment
This config is optimized for Railway and similar cloud platforms
"""
import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '8080')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', min(multiprocessing.cpu_count() * 2 + 1, 4)))
worker_class = 'gthread'
threads = int(os.getenv('GUNICORN_THREADS', 2))
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
keepalive = 5

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'academic-chatbot'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment if needed)
# keyfile = None
# certfile = None

# Security
forwarded_allow_ips = '*'
secure_scheme_headers = {'X-Forwarded-Proto': 'https'}

# Worker management
preload_app = True  # Load application code before worker processes are forked
reload = False  # Disable in production
