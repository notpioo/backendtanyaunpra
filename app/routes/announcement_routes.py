
from flask import Blueprint, request, jsonify
from app.services.announcement_service import announcement_service
from app.middleware.auth import login_required
from app.middleware.analytics import track_api_request

announcement_bp = Blueprint('announcement', __name__)

ALLOWED_CATEGORIES = ['Penting', 'Akademik', 'Umum', 'Info', 'Peraturan']

@announcement_bp.route('/', methods=['GET'])
@track_api_request
def get_all_announcements():
    """Get all announcements"""
    try:
        announcements = announcement_service.get_all_announcements()
        return jsonify({
            'success': True,
            'data': announcements
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@announcement_bp.route('/<announcement_id>', methods=['GET'])
def get_announcement(announcement_id):
    """Get announcement by ID"""
    try:
        announcement = announcement_service.get_announcement_by_id(announcement_id)
        if announcement:
            return jsonify({
                'success': True,
                'data': announcement
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Announcement not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@announcement_bp.route('/', methods=['POST'])
@login_required
def create_announcement():
    """Create new announcement"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON payload'
            }), 400
        
        title = data.get('title', '').strip()
        message = data.get('message', '').strip()
        category = data.get('category', 'Umum').strip()
        
        if not title or not message:
            return jsonify({
                'success': False,
                'error': 'Title and message are required'
            }), 400
        
        if category not in ALLOWED_CATEGORIES:
            return jsonify({
                'success': False,
                'error': f'Invalid category. Allowed: {", ".join(ALLOWED_CATEGORIES)}'
            }), 400
        
        new_announcement = announcement_service.create_announcement(title, message, category)
        
        if new_announcement:
            return jsonify({
                'success': True,
                'message': 'Announcement created successfully',
                'data': new_announcement
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create announcement'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@announcement_bp.route('/<announcement_id>', methods=['PUT'])
@login_required
def update_announcement(announcement_id):
    """Update announcement"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON payload'
            }), 400
        
        title = data.get('title', '').strip()
        message = data.get('message', '').strip()
        category = data.get('category', 'Umum').strip()
        
        if not title or not message:
            return jsonify({
                'success': False,
                'error': 'Title and message are required'
            }), 400
        
        if category not in ALLOWED_CATEGORIES:
            return jsonify({
                'success': False,
                'error': f'Invalid category. Allowed: {", ".join(ALLOWED_CATEGORIES)}'
            }), 400
        
        success = announcement_service.update_announcement(announcement_id, title, message, category)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Announcement updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update announcement or announcement not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@announcement_bp.route('/<announcement_id>', methods=['DELETE'])
@login_required
def delete_announcement(announcement_id):
    """Delete announcement"""
    try:
        success = announcement_service.delete_announcement(announcement_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Announcement deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete announcement or announcement not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
