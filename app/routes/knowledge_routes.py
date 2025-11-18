from flask import Blueprint, request, jsonify
from app.services.knowledge_service import knowledge_service
from app.services.cloudinary_service import CloudinaryService
from app.middleware.analytics import track_api_request

knowledge_bp = Blueprint('knowledge', __name__)
cloudinary_service = CloudinaryService()

@knowledge_bp.route('/', methods=['GET'])
@track_api_request
def get_all_knowledge():
    """Get all knowledge entries"""
    try:
        knowledge_list = knowledge_service.get_all_knowledge()
        return jsonify({
            'success': True,
            'data': knowledge_list,
            'total': len(knowledge_list)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@knowledge_bp.route('/<knowledge_id>', methods=['GET'])
def get_knowledge(knowledge_id):
    """Get single knowledge entry"""
    try:
        knowledge_item = knowledge_service.get_knowledge_by_id(knowledge_id)
        if knowledge_item:
            return jsonify({
                'success': True,
                'knowledge': knowledge_item
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Knowledge not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@knowledge_bp.route('/', methods=['POST'])
def add_knowledge():
    """Add new knowledge entry with optional image"""
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            question = data.get('question')
            answer = data.get('answer')
            category = data.get('category', 'general')
            keywords = data.get('keywords', '')
        else:
            # Access form fields directly to preserve file objects
            question = request.form.get('question')
            answer = request.form.get('answer')
            category = request.form.get('category', 'general')
            keywords = request.form.get('keywords', '')
        
        if not question or not answer:
            return jsonify({
                'success': False,
                'error': 'Question and answer are required'
            }), 400
        
        # Handle image upload if present
        image_url = ""
        image_public_id = ""
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                upload_result = cloudinary_service.upload_image(file)
                if upload_result:
                    image_url = upload_result['url']
                    image_public_id = upload_result['public_id']
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to upload image to Cloudinary'
                    }), 500
        
        success = knowledge_service.add_knowledge(
            question=question,
            answer=answer,
            category=category,
            keywords=keywords,
            image_url=image_url,
            image_public_id=image_public_id
        )
        
        if success:
            return jsonify({'success': True, 'message': 'Knowledge added successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to add knowledge'}), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@knowledge_bp.route('/<knowledge_id>', methods=['PUT', 'POST'])
def update_knowledge(knowledge_id):
    """Update existing knowledge entry with optional image"""
    try:
        # Get existing knowledge first to validate it exists
        existing_knowledge = knowledge_service.get_knowledge_by_id(knowledge_id)
        if not existing_knowledge:
            return jsonify({
                'success': False,
                'error': 'Knowledge not found'
            }), 404
        
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            question = data.get('question')
            answer = data.get('answer')
            category = data.get('category', 'general')
            keywords = data.get('keywords', '')
            # Normalize remove_image to handle both boolean and string
            remove_image_raw = data.get('remove_image', False)
            remove_image = remove_image_raw in [True, 'true', 'True', '1', 1]
        else:
            # Access form fields directly to preserve file objects
            question = request.form.get('question')
            answer = request.form.get('answer')
            category = request.form.get('category', 'general')
            keywords = request.form.get('keywords', '')
            # For form data, checkbox sends 'on' when checked, or field is absent
            remove_image_raw = request.form.get('remove_image', '')
            remove_image = remove_image_raw in ['on', 'true', 'True', '1']
        
        if not question or not answer:
            return jsonify({
                'success': False,
                'error': 'Question and answer are required'
            }), 400
        
        # Start with existing image data
        image_url = existing_knowledge.get('image_url', '')
        image_public_id = existing_knowledge.get('image_public_id', '')
        
        # Check if user wants to remove the image
        if remove_image and image_public_id:
            print(f"🗑️  Removing image: {image_public_id}")
            delete_success = cloudinary_service.delete_image(image_public_id)
            if not delete_success:
                return jsonify({
                    'success': False,
                    'error': 'Failed to delete image from Cloudinary. Please try again or contact support.'
                }), 500
            image_url = ""
            image_public_id = ""
        # Check if new image is uploaded
        elif 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                # Delete old image if exists
                if image_public_id:
                    print(f"🔄 Replacing old image: {image_public_id}")
                    delete_success = cloudinary_service.delete_image(image_public_id)
                    if not delete_success:
                        print(f"⚠️  Warning: Failed to delete old image {image_public_id}, but continuing with upload")
                        # Continue anyway - new image will replace the metadata
                
                # Upload new image
                upload_result = cloudinary_service.upload_image(file)
                if upload_result:
                    image_url = upload_result['url']
                    image_public_id = upload_result['public_id']
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to upload image to Cloudinary'
                    }), 500
        
        success = knowledge_service.update_knowledge(
            knowledge_id=knowledge_id,
            question=question,
            answer=answer,
            category=category,
            keywords=keywords,
            image_url=image_url,
            image_public_id=image_public_id
        )
        
        if success:
            return jsonify({'success': True, 'message': 'Knowledge updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update knowledge'}), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@knowledge_bp.route('/<knowledge_id>', methods=['DELETE'])
def delete_knowledge(knowledge_id):
    """Delete knowledge entry and associated image"""
    try:
        result = knowledge_service.delete_knowledge(knowledge_id)
        
        # If result is a string, it's the image public_id to delete
        if isinstance(result, str):
            cloudinary_service.delete_image(result)
            return jsonify({'success': True, 'message': 'Knowledge and image deleted successfully'})
        elif result:
            return jsonify({'success': True, 'message': 'Knowledge deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to delete knowledge'}), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@knowledge_bp.route('/stats', methods=['GET'])
def get_knowledge_stats():
    """Get knowledge statistics"""
    try:
        stats = knowledge_service.get_knowledge_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500