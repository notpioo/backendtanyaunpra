from flask import Blueprint, request, jsonify
from app.services.schedule_service import schedule_service
from app.middleware.auth import login_required
from app.middleware.analytics import track_api_request

schedule_bp = Blueprint('schedule', __name__)

@schedule_bp.route('/', methods=['GET'])
@track_api_request
def get_all_schedules():
    """Get all schedule events (for mobile app)"""
    try:
        schedules = schedule_service.get_all_schedules()
        return jsonify({
            'success': True,
            'data': schedules
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@schedule_bp.route('/range', methods=['GET'])
@track_api_request
def get_schedules_by_range():
    """Get schedules by date range (for mobile calendar view)"""
    try:
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')

        schedules = schedule_service.get_schedules_by_date_range(start_date, end_date)
        return jsonify({
            'success': True,
            'data': schedules
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@schedule_bp.route('/<schedule_id>', methods=['GET'])
@track_api_request
def get_schedule(schedule_id):
    """Get schedule by ID"""
    try:
        schedule = schedule_service.get_schedule_by_id(schedule_id)
        if schedule:
            return jsonify({
                'success': True,
                'data': schedule
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Schedule not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@schedule_bp.route('/', methods=['POST'])
@login_required
def create_schedule():
    """Create new schedule event (admin only)"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON payload'
            }), 400

        title = data.get('title', '').strip()
        start_date = data.get('start_date', '').strip()
        end_date = data.get('end_date', '').strip()

        # Validate required fields
        if not title or not start_date:
            return jsonify({
                'success': False,
                'error': 'Title and start_date are required'
            }), 400

        new_schedule = schedule_service.create_schedule(
            title=title,
            start_date=start_date,
            end_date=end_date if end_date else None
        )

        if new_schedule:
            return jsonify({
                'success': True,
                'message': 'Schedule created successfully',
                'data': new_schedule
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create schedule'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@schedule_bp.route('/<schedule_id>', methods=['PUT'])
@login_required
def update_schedule(schedule_id):
    """Update schedule event (admin only)"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON payload'
            }), 400

        title = data.get('title', '').strip()
        start_date = data.get('start_date', '').strip()
        end_date = data.get('end_date', '').strip()

        if not title or not start_date:
            return jsonify({
                'success': False,
                'error': 'Title and start_date are required'
            }), 400

        success = schedule_service.update_schedule(
            schedule_id=schedule_id,
            title=title,
            start_date=start_date,
            end_date=end_date if end_date else None
        )

        if success:
            return jsonify({
                'success': True,
                'message': 'Schedule updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update schedule or schedule not found'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@schedule_bp.route('/<schedule_id>', methods=['DELETE'])
@login_required
def delete_schedule(schedule_id):
    """Delete schedule event (admin only)"""
    try:
        success = schedule_service.delete_schedule(schedule_id)

        if success:
            return jsonify({
                'success': True,
                'message': 'Schedule deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete schedule or schedule not found'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@schedule_bp.route('/stats', methods=['GET'])
@track_api_request
def get_schedule_stats():
    """Get schedule statistics"""
    try:
        stats = schedule_service.get_schedule_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500