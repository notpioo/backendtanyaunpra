
from functools import wraps
from flask import request, g
from datetime import datetime
import time

def track_api_request(f):
    """Decorator to track API request analytics"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Record start time
        g.start_time = time.time()
        g.request_path = request.path
        g.request_method = request.method
        g.request_ip = request.remote_addr or 'unknown'
        g.request_user_agent = request.headers.get('User-Agent', 'unknown')
        
        # Execute the actual route function
        response = f(*args, **kwargs)
        
        # Record end time and calculate duration
        g.end_time = time.time()
        g.response_time = g.end_time - g.start_time
        
        # Get status code from response
        if hasattr(response, 'status_code'):
            g.status_code = response.status_code
        elif isinstance(response, tuple) and len(response) > 1:
            g.status_code = response[1]
        else:
            g.status_code = 200
        
        # Log analytics after response (non-blocking)
        try:
            from app.services.analytics_service import analytics_service
            analytics_service.log_request(
                endpoint=g.request_path,
                method=g.request_method,
                status_code=g.status_code,
                response_time=g.response_time,
                ip_address=g.request_ip,
                user_agent=g.request_user_agent
            )
        except Exception as e:
            # Don't let analytics errors break the API
            print(f"⚠️ Analytics logging error: {e}")
        
        return response
    
    return decorated_function
