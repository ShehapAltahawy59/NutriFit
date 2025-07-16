from fastapi import APIRouter, Request
from typing import List
import firebase_admin
from firebase_admin import messaging
from Agents.firebase_plans import ensure_firebase_initialized, send_plan_created_notification

router = APIRouter()

@router.post('/send_plan_notification')
async def send_plan_notification(request: Request):
    try:
        data = await request.json()
        if not data:
            return {"error": "No data provided"}
        user_id = data.get('user_id')
        if not user_id:
            return {"error": "user_id is required"}
        response = send_plan_created_notification(user_id)
        return {
            "status": "success",
            "message": "Notification sent successfully",
            "message_id": response
        }
    except Exception as e:
        return {"error": f"Failed to send notification: {str(e)}"}

@router.post('/send_custom_notification')
async def send_custom_notification(request: Request):
    try:
        data = await request.json()
        if not data:
            return {"error": "No data provided"}
        required_fields = ['user_id', 'title', 'body']
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}
        user_id = data['user_id']
        title = data['title']
        body = data['body']
        ensure_firebase_initialized()
        topic = str(user_id)
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            topic=topic
        )
        response = messaging.send(message)
        return {
            "status": "success",
            "message": "Custom notification sent successfully",
            "message_id": response
        }
    except Exception as e:
        return {"error": f"Failed to send custom notification: {str(e)}"}

@router.post('/send_bulk_notification')
async def send_bulk_notification(request: Request):
    try:
        data = await request.json()
        if not data:
            return {"error": "No data provided"}
        required_fields = ['user_ids', 'title', 'body']
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}
        user_ids = data['user_ids']
        title = data['title']
        body = data['body']
        if not isinstance(user_ids, list):
            return {"error": "user_ids must be a list"}
        ensure_firebase_initialized()
        responses = []
        for user_id in user_ids:
            try:
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
        return {
            "status": "completed",
            "results": responses
        }
    except Exception as e:
        return {"error": f"Failed to send bulk notification: {str(e)}"}

@router.get('/health')
async def notification_health_check():
    try:
        ensure_firebase_initialized()
        return {
            "status": "healthy",
            "service": "notification",
            "capabilities": [
                "send_plan_notification",
                "send_custom_notification",
                "send_bulk_notification"
            ]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "notification",
            "error": str(e)
        } 
