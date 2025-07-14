import os
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from firebase_admin import messaging

FIREBASE_JSON_PATH = '/app/secrets/firebase.json'

# Ensure Firebase is initialized

def ensure_firebase_initialized():
    if not firebase_admin._apps:
        # Write the service account JSON from the environment variable to a file (if running in Azure)
        firebase_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
        if firebase_json:
            os.makedirs(os.path.dirname(FIREBASE_JSON_PATH), exist_ok=True)
            with open(FIREBASE_JSON_PATH, 'w') as f:
                f.write(firebase_json)
        cred = credentials.Certificate(FIREBASE_JSON_PATH)
        firebase_admin.initialize_app(cred)

def get_firestore_client():
    ensure_firebase_initialized()
    return firestore.client()

PLANS_COLLECTION = 'plans'


def get_user_plans(user_id):
    db = get_firestore_client()
    """
    Retrieve the last plan for a given user based on createdAt.
    Args:
        user_id (str): The user's unique identifier
    Returns:
        dict: The last plan document with gymPlan and nutritionPlan, or None if no plans exist
    """
    plans_ref = db.collection(PLANS_COLLECTION)
    query = plans_ref.where('userId', '==', user_id).order_by('createdAt', direction=firestore.Query.DESCENDING).limit(1)
    docs = query.stream()
    
    for doc in docs:
        return {
            'gymPlan': doc.to_dict().get('gymPlan'),
            'nutritionPlan': doc.to_dict().get('nutritionPlan'),
            'inbody_data':doc.to_dict().get('inbody_data',''),
        }
    return None

def save_full_user_plan(user_id, gym_plan, nutrition_plan, image_url, is_viewed, subscription_type,time,inbody_data):
    db = get_firestore_client()
    """
    Save a new plan for a user with the full schema.
    Args:
        user_id (str): The user's unique identifier
        gym_plan (dict): The gym plan data
        nutrition_plan (dict): The nutrition plan data
        image_url (str): The image URL
        is_viewed (bool): Whether the plan has been viewed
        subscription_type (int): The subscription type
    Returns:
        str: The document ID of the saved plan
    """
    doc_ref = db.collection(PLANS_COLLECTION).document()
    doc_ref.set({
        'userId': user_id,
        'gymPlan': gym_plan,
        'nutritionPlan': nutrition_plan,
        'createdAt': time,
        'imageUrl': image_url,
        'isViewed': is_viewed,
        'subscriptionType': subscription_type,
        'inbody_data':inbody_data
    })
    return doc_ref.id 

def increment_used_requests(user_id):
    db = get_firestore_client()
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        subscription = user_data.get('subscription', {})
        used_requests = subscription.get('usedRequests', 0)
        # Increment
        subscription['usedRequests'] = used_requests + 1
        user_ref.update({'subscription': subscription})
     

def send_plan_created_notification(user_id):
    ensure_firebase_initialized()
    topic = str(user_id)
    message = messaging.Message(
        notification=messaging.Notification(
            title='Your Plans Are Ready!',
            body='Your gym and nutrition plans have been created. Check them now!'
        ),
        topic=topic
    )
    response = messaging.send(message)
    return response
     
