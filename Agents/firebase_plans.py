import os
import firebase_admin
from firebase_admin import credentials, firestore

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
    Retrieve all plans for a given user.
    Args:
        user_id (str): The user's unique identifier
    Returns:
        list: A list of plan documents (dicts) with only gymPlan and nutritionPlan
    """
    plans_ref = db.collection(PLANS_COLLECTION)
    query = plans_ref.where('userId', '==', user_id)
    docs = query.stream()
    return [
        {
            'gymPlan': doc.to_dict().get('gymPlan'),
            'nutritionPlan': doc.to_dict().get('nutritionPlan'),
        }
        for doc in docs
    ] 
