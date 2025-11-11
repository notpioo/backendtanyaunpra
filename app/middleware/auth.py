
import os
from functools import wraps
from flask import session, redirect, url_for, request

def login_required(f):
    """Decorator to protect admin routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def check_admin_credentials(username, password):
    """Verify admin credentials from environment variables"""
    # Use os.environ to ensure we get the actual environment values
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    
    # Debug logging
    print(f"🔐 Login attempt - Username: {username}")
    print(f"🔐 Expected username: {admin_username}")
    print(f"🔐 Password configured: {'Yes' if admin_password else 'No (using default)'}")
    
    if not admin_password:
        # Fallback default (HARUS DIGANTI DI PRODUCTION!)
        admin_password = 'admin123'
        print("⚠️ WARNING: Using default admin password! Set ADMIN_PASSWORD in environment variables!")
    
    # Validate both username AND password must match
    is_valid = (username == admin_username and password == admin_password)
    print(f"🔐 Login result: {'✅ SUCCESS' if is_valid else '❌ FAILED'}")
    
    return is_valid
