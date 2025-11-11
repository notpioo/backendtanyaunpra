import os
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from app.services.knowledge_service import knowledge_service
from app.services.announcement_service import announcement_service
from app.middleware.auth import login_required, check_admin_credentials

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def landing():
    """Public landing page"""
    return render_template('landing.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    # If already logged in, redirect to dashboard
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if check_admin_credentials(username, password):
            session['admin_logged_in'] = True
            session.permanent = True  # Make session persistent
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Username atau password salah!', 'error')
            return render_template('login.html'), 401

    return render_template('login.html')

@admin_bp.route('/logout')
def logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('admin.landing'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    try:
        stats = knowledge_service.get_knowledge_stats()
        announcement = announcement_service.get_current_announcement()
        return render_template('dashboard.html', stats=stats, announcement=announcement)
    except Exception as e:
        return render_template('dashboard.html', stats={'total_knowledge': 0, 'categories': {}}, announcement={'title': 'Announcement', 'message': 'No announcement available'})

@admin_bp.route('/knowledge')
@login_required
def knowledge_management():
    """Knowledge management page"""
    try:
        knowledge_list = knowledge_service.get_all_knowledge()
        return render_template('knowledge.html', knowledge_list=knowledge_list)
    except Exception as e:
        return render_template('knowledge.html', knowledge_list=[])

@admin_bp.route('/testing')
@login_required
def chatbot_testing():
    """Chatbot testing page"""
    return render_template('testing.html')

@admin_bp.route('/models')
@login_required
def models():
    """Models management page"""
    return render_template('models.html')

@admin_bp.route('/announcement')
@login_required
def announcement():
    """Announcement management page"""
    return render_template('announcement.html')

@admin_bp.route('/api-docs')
@login_required
def api_docs():
    """API documentation page"""
    return render_template('api_docs.html')

@admin_bp.route('/settings')
@login_required
def settings():
    """Settings page"""
    return render_template('settings.html')

@admin_bp.route('/api/models/current-api-key')
@login_required
def get_current_api_key():
    """Get current GEMINI API key status"""
    try:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if api_key:
            # Return masked version for display and full key for visibility toggle
            if len(api_key) > 10:
                masked_key = api_key[:6] + '•' * (len(api_key) - 10) + api_key[-4:]
            else:
                masked_key = '•' * len(api_key)

            return jsonify({
                "success": True,
                "api_key": masked_key,  # Masked version for default display
                "full_api_key": api_key,  # Full key for unhide functionality
                "has_key": True,
                "key_length": len(api_key)
            })
        else:
            return jsonify({
                "success": False,
                "message": "No API key configured",
                "api_key": "",
                "full_api_key": "",
                "has_key": False
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e),
            "api_key": "",
            "full_api_key": "",
            "has_key": False
        }), 500

def update_env_file(key, value):
    """Update .env file with new key-value pair"""
    try:
        env_file_path = '.env'

        # Read current .env file if exists
        env_lines = []
        key_found = False

        if os.path.exists(env_file_path):
            with open(env_file_path, 'r') as f:
                env_lines = f.readlines()

        # Update or add the key
        new_lines = []
        for line in env_lines:
            if line.strip().startswith(f'{key}='):
                new_lines.append(f'{key}={value}\n')
                key_found = True
            else:
                new_lines.append(line)

        # Add key if not found
        if not key_found:
            new_lines.append(f'{key}={value}\n')

        # Write back to .env file
        with open(env_file_path, 'w') as f:
            f.writelines(new_lines)

        return True

    except Exception as e:
        print(f"Warning: Could not update .env file: {e}")
        return False

@admin_bp.route('/api/models/update-api-key', methods=['POST'])
@login_required
def update_api_key():
    """Update GEMINI API key in both runtime and .env file"""
    try:
        data = request.get_json()
        new_api_key = data.get('api_key', '').strip()

        if not new_api_key:
            return jsonify({
                "success": False,
                "message": "API key cannot be empty"
            }), 400

        # Validate API key format (basic validation)
        if not new_api_key.startswith('AIza') or len(new_api_key) < 30:
            return jsonify({
                "success": False,
                "message": "Invalid API key format. GEMINI API keys should start with 'AIza'"
            }), 400

        # Test the API key first by trying to initialize the service
        old_key = os.environ.get("GEMINI_API_KEY")  # Store original key

        try:
            # Temporarily set the new key for testing
            os.environ["GEMINI_API_KEY"] = new_api_key

            from app.services.gemini_service import GeminiService
            test_service = GeminiService()

        except Exception as api_error:
            # Restore old key if test failed
            if old_key:
                os.environ["GEMINI_API_KEY"] = old_key
            else:
                os.environ.pop("GEMINI_API_KEY", None)

            return jsonify({
                "success": False,
                "message": f"API key validation failed: {str(api_error)}"
            }), 400

        # If test successful, update persistent storage
        update_messages = []

        # Update .env file if possible
        env_updated = update_env_file("GEMINI_API_KEY", new_api_key)
        if env_updated:
            update_messages.append("Updated .env file")
        else:
            update_messages.append("Runtime environment updated (use Replit Secrets for persistence)")

        # Reload the service with new key
        try:
            from app.services.gemini_service import gemini_service
            gemini_service.reload_api_key()
        except Exception as e:
            print(f"Warning: Could not reload Gemini service: {e}")

        message = "API key updated successfully! " + ", ".join(update_messages)

        return jsonify({
            "success": True,
            "message": message,
            "env_file_updated": env_updated
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500