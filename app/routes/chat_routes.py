from flask import Blueprint, request, jsonify
from datetime import datetime
from app.services.gemini_service import gemini_service
from app.services.knowledge_service import knowledge_service
from app.middleware.analytics import track_api_request

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/message', methods=['POST'])
@track_api_request
def process_message():
    """Process chat message from Flutter app"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        user_message = data['message']
        
        # Check if message is academically relevant
        if not gemini_service.check_academic_relevance(user_message):
            return jsonify({
                'success': True,
                'response': 'Maaf, saya hanya dapat membantu dengan pertanyaan yang berkaitan dengan akademik, pembelajaran, dan informasi kampus. Silakan ajukan pertanyaan seputar topik tersebut.',
                'source': 'filter'
            })
        
        # Search for relevant knowledge in database
        knowledge_result = knowledge_service.search_knowledge(user_message)
        knowledge_context = knowledge_result.get('context', '')
        knowledge_image_url = knowledge_result.get('image_url', '')
        
        # Generate response using Gemini
        ai_response = gemini_service.generate_response(user_message, knowledge_context)
        
        # Add image URL to response if available
        if knowledge_image_url:
            ai_response['image_url'] = knowledge_image_url
        
        return jsonify(ai_response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'response': 'Maaf, terjadi kesalahan sistem. Silakan coba lagi.',
            'error': str(e)
        }), 500

@chat_bp.route('/health', methods=['GET'])
@track_api_request
def health_check():
    """API health check endpoint"""
    try:
        # Test Gemini service connectivity
        from app.services.gemini_service import gemini_service
        
        from datetime import timezone, timedelta
        WIB = timezone(timedelta(hours=7))
        
        return jsonify({
            'success': True,
            'status': 'online',
            'service': 'academic-chatbot-api',
            'message': 'API is running successfully',
            'timestamp': datetime.now(WIB).isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'error',
            'message': str(e)
        }), 500