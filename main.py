from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import base64
import json

# Import agent routers (converted from Flask blueprints to FastAPI routers)
from Agents.v2.inbody_specialist import router as inbody_router_v2
from Agents.v2.nutritionist import router as nutritionist_router_v2
from Agents.v2.gym_trainer import router as gym_trainer_router_v2
from Agents.v2.plan_workflow import router as workflow_router_v2
from Agents.v2.notification import router as notification_router_v2

from Agents.v1.nutritionist import router as nutritionist_router_v1
from Agents.v1.gym_trainer import router as gym_trainer_router_v1
from Agents.v1.inbody_specialist import router as inbody_router_v1
from Agents.v1.plan_workflow import router as workflow_router_v1
from Agents.v1.notification import router as notification_router_v1
from Agents.v1.summerizer import router as summerizer_router_v1  # if needed

# Load environment variables
load_dotenv()

import firebase_admin
from firebase_admin import credentials, firestore

firebase_json_b64 = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
if firebase_json_b64:
    print("FIREBASE_SERVICE_ACCOUNT_JSON present:", bool(firebase_json_b64))
    try:
        service_account_info = json.loads(base64.b64decode(firebase_json_b64).decode('utf-8'))
    except Exception as e:
        print("Error decoding FIREBASE_SERVICE_ACCOUNT_JSON:", e)
        raise
else:
    raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_JSON environment variable not set")

cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with URL prefixes
app.include_router(inbody_router_v2, prefix="/api/v2/inbody")
app.include_router(nutritionist_router_v2, prefix="/api/v2/nutritionist")
app.include_router(gym_trainer_router_v2, prefix="/api/v2/gym")
app.include_router(workflow_router_v2, prefix="/api/v2/workflow")
app.include_router(notification_router_v2, prefix="/api/v2/notification")

app.include_router(nutritionist_router_v1, prefix="/api/v1/nutritionist")
app.include_router(gym_trainer_router_v1, prefix="/api/v1/gym")
app.include_router(inbody_router_v1, prefix="/api/v1/inbody")
app.include_router(workflow_router_v1, prefix="/api/v1/workflow")
app.include_router(notification_router_v1, prefix="/api/v1/notification")
# app.include_router(summerizer_router_v1, prefix="/api/v1/summerizer")  # if needed

@app.get("/health")
def health_check():
    return {
        "status": "so healthy",
        "service": "nutrifit_agents",
        "timestamp": "2024-01-01T00:00:00Z",
        "agents": {
            "inbody_specialist": "/inbody/health",
            "nutritionist": "/nutritionist/health",
            "gym_trainer": "/gym/health",
            "plan_workflow": "/workflow/health"
        },
        "version": "2.3.0"
    }

@app.get("/ping")
def ping():
    return {
        "status": "pong",
        "message": "NutriFit Agents API is running"
    }

@app.get("/status")
def status():
    # You may want to implement agent checks here as in Flask, or simplify
    return {
        "overall_status": "healthy",
        "api_info": {
            "version": "1.0.0",
            "description": "NutriFit Agents API - Comprehensive nutrition and fitness planning"
        }
    }

@app.get("/")
def documentation():
    return {
        "welcome": "NutriFit Agents API",
        "description": "Comprehensive nutrition and fitness planning using AI agents",
        "version": "1.0.0",
        "endpoints": {
            "main": {
                "GET /": "This documentation",
                "GET /health": "Main health check",
                "GET /status": "Detailed agent status"
            },
            "inbody_specialist": {
                "POST /inbody/analyze": "Comprehensive body composition analysis",
                "POST /inbody/simple_analysis": "Quick InBody analysis",
                "GET /inbody/health": "InBody specialist health check"
            },
            "nutritionist": {
                "POST /nutritionist/create_plan": "Comprehensive nutrition plan with evaluation",
                "POST /nutritionist/simple_plan": "Simple nutrition plan",
                "POST /nutritionist/advice": "General nutrition advice",
                "GET /nutritionist/health": "Nutritionist health check"
            },
            "gym_trainer": {
                "POST /gym/create_workout": "Comprehensive workout plan",
                "POST /gym/simple_workout": "Simple workout plan",
                "POST /gym/exercise_advice": "Exercise-specific advice",
                "POST /gym/form_check": "Exercise form analysis (requires image)",
                "GET /gym/health": "Gym trainer health check"
            },
            "plan_workflow": {
                "POST /workflow/create_complete_plan": "Complete workflow from InBody image to nutrition plan",
                "GET /workflow/workflow_status": "Workflow status and capabilities",
                "POST /workflow/test_inbody_analysis": "Test InBody analysis only",
                "GET /workflow/health": "Workflow health check"
            }
        },
        "usage_examples": {
            "complete_workflow": {
                "endpoint": "POST /workflow/create_complete_plan",
                "body": {
                    "inbody_image_url": "https://example.com/inbody-scan.jpg",
                    "client_country": "Egypt",
                    "goals": "Weight loss and muscle building",
                    "allergies": "Lactose intolerant",
                    "user_info": "Age: 30, Weight: 70kg, Height: 170cm"
                }
            },
            "inbody_analysis": {
                "endpoint": "POST /inbody/analyze",
                "body": {
                    "user_info": "Age: 30, Weight: 70kg, Height: 170cm",
                    "scan_data": "InBody scan results...",
                    "goals": "Weight loss and muscle building"
                }
            },
            "nutrition_plan": {
                "endpoint": "POST /nutritionist/create_plan",
                "body": {
                    "user_info": "Age: 30, Weight: 70kg, Height: 170cm",
                    "goals": "Weight loss",
                    "allergies": "Lactose intolerant"
                }
            },
            "workout_plan": {
                "endpoint": "POST /gym/create_workout",
                "body": {
                    "user_info": "Age: 30, Weight: 70kg, Height: 170cm",
                    "fitness_level": "intermediate",
                    "goals": "Muscle building",
                    "preferences": "Strength training",
                    "available_equipment": "Full gym access"
                }
            }
        },
        "workflow_description": {
            "complete_plan_workflow": {
                "description": "End-to-end nutrition planning from InBody scan to validated diet plan",
                "steps": [
                    "1. InBody image analysis and data extraction",
                    "2. Nutrition plan creation with cultural adaptation",
                    "3. Plan evaluation and validation"
                ],
                "inputs": [
                    "inbody_image_url (required)",
                    "client_country (required)",
                    "goals (required)",
                    "allergies (optional)",
                    "user_info (optional)"
                ],
                "outputs": [
                    "inbody_analysis: Extracted body composition data",
                    "nutrition_plan: 4-week validated diet plan",
                    "workflow_steps: Detailed execution status"
                ]
            }
        }
    } 
