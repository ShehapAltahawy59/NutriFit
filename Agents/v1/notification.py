from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import firebase_admin
from firebase_admin import messaging
from Agents.firebase_plans import ensure_firebase_initialized, send_plan_created_notification

# Create Blueprint for Notifications
notification_bp = Blueprint('notification_v1', __name__)

@notification_bp.route('/send_plan_notification', methods=['POST'])
@cross_origin()
def send_plan_notification():
    """Send notification when plans are created"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        # Send notification
        response = send_plan_created_notification(user_id)
        
        return jsonify({
            "status": "success",
            "message": "Notification sent successfully",
            "message_id": response
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to send notification: {str(e)}"}), 500

@notification_bp.route('/send_custom_notification', methods=['POST'])
@cross_origin()
def send_custom_notification():
    """Send custom notification to a user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['user_id', 'title', 'body']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        user_id = data['user_id']
        title = data['title']
        body = data['body']
        
        # Ensure Firebase is initialized
        ensure_firebase_initialized()
        
        # Create topic from user_id
        topic = str(user_id)
        
        # Create and send message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            topic=topic
        )
        
        response = messaging.send(message)
        
        return jsonify({
            "status": "success",
            "message": "Custom notification sent successfully",
            "message_id": response
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to send custom notification: {str(e)}"}), 500

@notification_bp.route('/send_bulk_notification', methods=['POST'])
@cross_origin()
def send_bulk_notification():
    """Send notification to multiple users"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['user_ids', 'title', 'body']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        user_ids = data['user_ids']
        title = data['title']
        body = data['body']
        
        if not isinstance(user_ids, list):
            return jsonify({"error": "user_ids must be a list"}), 400
        
        # Ensure Firebase is initialized
        ensure_firebase_initialized()
        
        # Create message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            topic='general'  # You might want to use a different topic for bulk notifications
        )
        
        # Send to each user
        responses = []
        for user_id in user_ids:
            try:
                # Create user-specific topic
                topic = str(user_id)
                user_message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body
                    ),
                    topic=topic
                )
                response = messaging.send(user_message)
                responses.append({"user_id": user_id, "status": "success", "message_id": response})
            except Exception as e:
                responses.append({"user_id": user_id, "status": "failed", "error": str(e)})
        
        return jsonify({
            "status": "completed",
            "results": responses
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to send bulk notification: {str(e)}"}), 500

@notification_bp.route('/health', methods=['GET'])
@cross_origin()
def notification_health_check():
    """Health check endpoint for Notification service"""
    try:
        # Check if Firebase is initialized
        ensure_firebase_initialized()
        
        return jsonify({
            "status": "healthy",
            "service": "notification",
            "capabilities": [
                "send_plan_notification",
                "send_custom_notification", 
                "send_bulk_notification"
            ]
        })
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "service": "notification",
            "error": str(e)
        }), 500 
