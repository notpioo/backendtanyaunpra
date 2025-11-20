import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.routes.admin_routes import admin_bp
from app.routes.chat_routes import chat_bp
from app.routes.knowledge_routes import knowledge_bp
from app.routes.announcement_routes import announcement_bp
from app.routes.schedule_routes import schedule_bp
from app.config.firebase_config import initialize_firebase

# Load environment variables from .env file with priority
# override=True means .env file takes priority over existing env vars (including Replit Secrets)
load_dotenv(dotenv_path='.env', override=True)

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

    # Configure Flask - require SESSION_SECRET for security
    session_secret = os.getenv('SESSION_SECRET')
    if not session_secret:
        raise ValueError("SESSION_SECRET is required. Add it to Replit secrets or .env file")
    app.config['SECRET_KEY'] = session_secret
    app.config['JSON_AS_ASCII'] = False  # Support Indonesian characters

    # Configure CORS with restricted origins for security
    allowed_origins = os.getenv('ALLOWED_ORIGINS', '').split(',') if os.getenv('ALLOWED_ORIGINS') else ['*']
    if allowed_origins == ['*']:
        print("⚠️  Warning: CORS allows all origins. Set ALLOWED_ORIGINS in production for security.")
    CORS(app, origins=allowed_origins)

    # Initialize Firebase
    try:
        initialize_firebase()
        print("✅ Firebase initialized successfully")
    except Exception as e:
        print(f"❌ Firebase initialization error: {e}")

    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')
    app.register_blueprint(admin_bp, url_prefix='/')
    app.register_blueprint(announcement_bp, url_prefix='/api/announcement')
    app.register_blueprint(schedule_bp, url_prefix='/api/schedule')

    return app

if __name__ == '__main__':
    import logging
    
    # Configure logging and debug mode based on environment
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logging.basicConfig(level=log_level)
    
    app = create_app()
    # Use localhost for local development, 0.0.0.0 for Replit/production
    host = os.getenv('FLASK_HOST', '0.0.0.0')  # Default 0.0.0.0 for Replit
    app.run(host=host, port=5000, debug=debug_mode)