from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import agent blueprints
from Agents.v1.inbody_specialist import inbody_bp
from Agents.v1.nutritionist import nutritionist_bp
from Agents.v1.gym_trainer import gym_trainer_bp
from Agents.v1.plan_workflow import workflow_bp
from Agents.v1.notification import notification_bp

from Agents.v2.inbody_specialist import inbody_bp as inbody_bp_v2
from Agents.v2.nutritionist import nutritionist_bp as nutritionist_bp_v2
from Agents.v2.gym_trainer import gym_trainer_bp as gym_trainer_bp_v2
from Agents.v2.plan_workflow import workflow_bp as workflow_bp_v2
from Agents.v2.notification import notification_bp as notification_bp_v2
# Load environment variables
load_dotenv()

import firebase_admin
from firebase_admin import credentials, firestore

import os
import base64
import json

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


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, resources={
        r"/*": {
            "origins": ["*"],  # Allow all origins in development
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
        }
    })
    
    # Register blueprints with URL prefixes
    app.register_blueprint(inbody_bp, url_prefix='/api/v1/inbody')
    app.register_blueprint(nutritionist_bp, url_prefix='/api/v1/nutritionist')
    app.register_blueprint(gym_trainer_bp, url_prefix='/api/v1/gym')
    app.register_blueprint(workflow_bp, url_prefix='/api/v1/workflow')
    app.register_blueprint(notification_bp, url_prefix='/api/v1/notification')

    app.register_blueprint(inbody_bp_v2, url_prefix='/api/v2/inbody')
    app.register_blueprint(nutritionist_bp_v2, url_prefix='/api/v2/nutritionist')
    app.register_blueprint(gym_trainer_bp_v2, url_prefix='/api/v2/gym')
    app.register_blueprint(workflow_bp_v2, url_prefix='/api/v2/workflow')
    app.register_blueprint(notification_bp_v2, url_prefix='/api/v2/notification')
    
    # Main health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Main health check endpoint"""
        return jsonify({
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
        })
    
    # Simple health check endpoint (no agent dependencies)
    @app.route('/ping', methods=['GET'])
    def ping():
        """Simple ping endpoint for basic connectivity"""
        return jsonify({
            "status": "pong",
            "message": "NutriFit Agents API is running"
        })
    
    # Main status endpoint
    @app.route('/status', methods=['GET'])
    def status():
        """Get status of all agents"""
        try:
            # Import here to avoid circular imports (using absolute imports)
            from Agents.v1.inbody_specialist import create_inbody_agent
            from Agents.v1.nutritionist import create_nutritionist_agent, create_evaluator_agent
            from Agents.v1.gym_trainer import create_gym_trainer_agent
            
            # Check each agent
            inbody_agent = create_inbody_agent()
            nutritionist_agent = create_nutritionist_agent()
            evaluator_agent = create_evaluator_agent()
            gym_trainer_agent = create_gym_trainer_agent()
            
            status = {
                "overall_status": "healthy" if all([inbody_agent, nutritionist_agent, evaluator_agent, gym_trainer_agent]) else "unhealthy",
                "agents": {
                    "inbody_specialist": {
                        "status": "available" if inbody_agent else "unavailable",
                        "endpoints": [
                            "/inbody/analyze",
                            "/inbody/simple_analysis",
                            "/inbody/health"
                        ]
                    },
                    "nutritionist": {
                        "status": "available" if nutritionist_agent else "unavailable",
                        "endpoints": [
                            "/nutritionist/create_plan",
                            "/nutritionist/simple_plan",
                            "/nutritionist/advice",
                            "/nutritionist/health"
                        ]
                    },
                    "evaluator": {
                        "status": "available" if evaluator_agent else "unavailable",
                        "description": "Works with nutritionist for plan validation"
                    },
                    "gym_trainer": {
                        "status": "available" if gym_trainer_agent else "unavailable",
                        "endpoints": [
                            "/gym/create_workout",
                            "/gym/simple_workout",
                            "/gym/exercise_advice",
                            "/gym/form_check",
                            "/gym/health"
                        ]
                    }
                },
                "workflows": {
                    "complete_plan_workflow": {
                        "status": "available" if all([inbody_agent, nutritionist_agent, evaluator_agent]) else "unavailable",
                        "endpoints": [
                            "/workflow/create_complete_plan",
                            "/workflow/workflow_status",
                            "/workflow/test_inbody_analysis",
                            "/workflow/health"
                        ],
                        "description": "Complete pipeline from InBody image to nutrition plan"
                    }
                },
                "api_info": {
                    "version": "1.0.0",
                    "description": "NutriFit Agents API - Comprehensive nutrition and fitness planning"
                }
            }
            
            return jsonify(status)
            
        except Exception as e:
            return jsonify({
                "overall_status": "unhealthy",
                "error": f"Error checking agent status: {str(e)}"
            }), 500
    
    # Main documentation endpoint
    @app.route('/', methods=['GET'])
    def documentation():
        """API documentation and usage information"""
        return jsonify({
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
        })
    
    return app

# Create the application instance
app = create_app()

# For gunicorn compatibility
application = app

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the Flask app (production mode)
    app.run(
        debug=False,  # Disable debug mode for production
        host='0.0.0.0', 
        port=port
    ) 
