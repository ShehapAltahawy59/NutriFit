from flask import Blueprint, request, jsonify
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_core.models import UserMessage
from autogen_core import Image as AGImage
from PIL import Image
from autogen_agentchat.messages import MultiModalMessage
from io import BytesIO
import requests
import asyncio
from pydantic import BaseModel
from typing import List, Optional
from . import initialize_azure_client

# Create Blueprint for Gym Trainer
gym_trainer_bp = Blueprint('gym_trainer', __name__)

# Pydantic models for fitness training
class Exercise(BaseModel):
    name: str
    sets: int
    reps: int
    weight: Optional[str] = ""
    rest_time: str = "60 seconds"
    notes: Optional[str] = ""

class WorkoutDay(BaseModel):
    day: str
    focus: str
    exercises: List[Exercise]
    duration: str
    intensity: str

class WeeklyWorkoutPlan(BaseModel):
    week: str
    days: List[WorkoutDay]
    goals: str
    notes: str

class FitnessRequest(BaseModel):
    user_info: str
    fitness_level: str
    goals: str
    preferences: str
    restrictions: str = ""
    available_equipment: str = ""
    time_availability: str = ""
    image_url: str = ""

class FitnessResponse(BaseModel):
    workout_plan: dict
    recommendations: str
    status: str

def create_gym_trainer_agent():
    """Create and return the Gym Trainer agent"""
    client = initialize_azure_client()
    if not client:
        return None
    
    GymTrainer = AssistantAgent(
        name="GymTrainer",
        system_message="""You are a certified fitness trainer specializing in:
        - Exercise recommendations that complement nutrition plans
        - Workout routines for different fitness levels (beginner, intermediate, advanced)
        - Strength training and cardio guidance
        - Recovery and injury prevention
        - Bodyweight exercises and gym-based workouts
        - Progressive overload principles
        - Form and technique guidance
        - Workout periodization and planning
        - Functional fitness and mobility training
        - Sports-specific training programs
        
        Provide safe, effective exercise recommendations that support nutritional goals.
        Always consider the user's fitness level, available equipment, and time constraints.
        Format your responses with clear workout plans, exercise descriptions, and safety tips.""",
        model_client=client
    )
    
    return GymTrainer

async def process_fitness_image(image_url):
    """Process and analyze fitness-related image if provided"""
    if not image_url:
        return None
    
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Convert to PIL Image
        image = Image.open(BytesIO(response.content))
        
        # Convert to AutoGen Image format
        ag_image = AGImage.from_pil_image(image)
        
        return ag_image
    except Exception as e:
        print(f"Error processing fitness image: {e}")
        return None

async def create_comprehensive_workout_plan(user_info, fitness_level, goals, preferences, restrictions="", available_equipment="", time_availability="", image_url=""):
    """Create a comprehensive workout plan"""
    try:
        # Initialize Gym Trainer agent
        gym_trainer = create_gym_trainer_agent()
        
        if not gym_trainer:
            return {"error": "Failed to initialize Gym Trainer agent"}
        
        # Process image if provided
        image = await process_fitness_image(image_url)
        
        # Prepare workout plan message
        workout_message = f"""
        User Information: {user_info}
        Fitness Level: {fitness_level}
        Goals: {goals}
        Preferences: {preferences}
        Restrictions: {restrictions}
        Available Equipment: {available_equipment}
        Time Availability: {time_availability}
        
        Please create a comprehensive workout plan that includes:
        1. Weekly workout schedule with specific exercises
        2. Exercise descriptions with proper form cues
        3. Sets, reps, and rest periods
        4. Progressive overload recommendations
        5. Warm-up and cool-down routines
        6. Injury prevention tips
        7. Recovery strategies
        8. Modifications for different fitness levels
        9. Equipment alternatives if needed
        10. Progress tracking methods
        """
        
        # Create multimodal message with image
        message = MultiModalMessage(content=workout_message, source="User", images=[image])
        
        # Get workout plan from Gym Trainer
        workout_output = await gym_trainer.on_messages(
            message, 
            cancellation_token=CancellationToken()
        )
        
        # Extract the response
        if workout_output and len(workout_output) > 0:
            response = workout_output[-1].content
        else:
            response = "Unable to generate workout plan"
        
        return {
            "workout_plan": response,
            "recommendations": "Workout plan generated successfully",
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": f"Error creating workout plan: {str(e)}",
            "status": "error"
        }

async def create_simple_workout_plan(user_info, fitness_level, goals, preferences, restrictions=""):
    """Create a simple workout plan"""
    try:
        # Initialize Gym Trainer agent
        gym_trainer = create_gym_trainer_agent()
        
        if not gym_trainer:
            return {"error": "Failed to initialize Gym Trainer agent"}
        
        # Prepare simple workout message
        workout_message = f"""
        User Information: {user_info}
        Fitness Level: {fitness_level}
        Goals: {goals}
        Preferences: {preferences}
        Restrictions: {restrictions}
        
        Please provide a simple workout plan with basic exercises and recommendations.
        Focus on fundamental movements and safety.
        """
        
        # Get workout plan from Gym Trainer
        workout_output = await gym_trainer.on_messages(
            UserMessage(content=workout_message),
            cancellation_token=CancellationToken()
        )
        
        # Extract the response
        if workout_output and len(workout_output) > 0:
            response = workout_output[-1].content
        else:
            response = "Unable to generate workout plan"
        
        return {
            "workout_plan": response,
            "recommendations": "Simple workout plan generated successfully",
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": f"Error creating simple workout plan: {str(e)}",
            "status": "error"
        }

async def get_exercise_advice(query):
    """Get specific exercise advice"""
    try:
        # Initialize Gym Trainer agent
        gym_trainer = create_gym_trainer_agent()
        
        if not gym_trainer:
            return {"error": "Failed to initialize Gym Trainer agent"}
        
        # Get advice from Gym Trainer
        advice_output = await gym_trainer.on_messages(
            UserMessage(content=query),
            cancellation_token=CancellationToken()
        )
        
        # Extract the response
        if advice_output and len(advice_output) > 0:
            response = advice_output[-1].content
        else:
            response = "Unable to generate exercise advice"
        
        return {
            "advice": response,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": f"Error getting exercise advice: {str(e)}",
            "status": "error"
        }

# Flask routes for Gym Trainer
@gym_trainer_bp.route('/create_workout', methods=['POST'])
def create_workout_plan():
    """Main endpoint for creating comprehensive workout plans"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['user_info', 'fitness_level', 'goals', 'preferences']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Extract data
        user_info = data['user_info']
        fitness_level = data['fitness_level']
        goals = data['goals']
        preferences = data['preferences']
        restrictions = data.get('restrictions', '')
        available_equipment = data.get('available_equipment', '')
        time_availability = data.get('time_availability', '')
        image_url = data.get('image_url', '')
        
        # Create workout plan
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                create_comprehensive_workout_plan(user_info, fitness_level, goals, preferences, restrictions, available_equipment, time_availability, image_url)
            )
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@gym_trainer_bp.route('/simple_workout', methods=['POST'])
def create_simple_workout():
    """Endpoint for creating simple workout plans"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['user_info', 'fitness_level', 'goals', 'preferences']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Extract data
        user_info = data['user_info']
        fitness_level = data['fitness_level']
        goals = data['goals']
        preferences = data['preferences']
        restrictions = data.get('restrictions', '')
        
        # Create simple workout plan
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                create_simple_workout_plan(user_info, fitness_level, goals, preferences, restrictions)
            )
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@gym_trainer_bp.route('/exercise_advice', methods=['POST'])
def exercise_advice():
    """Endpoint for exercise-specific advice"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({"error": "Query is required"}), 400
        
        query = data['query']
        
        # Get exercise advice
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                get_exercise_advice(query)
            )
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@gym_trainer_bp.route('/form_check', methods=['POST'])
def form_check():
    """Endpoint for exercise form analysis (if image provided)"""
    try:
        data = request.get_json()
        
        if not data or 'exercise' not in data:
            return jsonify({"error": "Exercise name is required"}), 400
        
        exercise = data['exercise']
        image_url = data.get('image_url', '')
        
        if not image_url:
            return jsonify({"error": "Image URL is required for form check"}), 400
        
        # Initialize Gym Trainer agent
        gym_trainer = create_gym_trainer_agent()
        
        if not gym_trainer:
            return jsonify({"error": "Failed to initialize Gym Trainer agent"}), 500
        
        # Process image and get form analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            image = loop.run_until_complete(process_fitness_image(image_url))
            
            if not image:
                return jsonify({"error": "Failed to process image"}), 400
            
            form_message = f"""
            Please analyze the form for the exercise: {exercise}
            
            Provide feedback on:
            1. Overall form quality
            2. Specific areas for improvement
            3. Safety concerns
            4. Tips for better execution
            5. Common mistakes to avoid
            """
            
            # Create multimodal message with image
            message = MultiModalMessage(content=form_message, source="User", images=[image])
            
            form_output = loop.run_until_complete(
                gym_trainer.on_messages(message, cancellation_token=CancellationToken())
            )
            
            if form_output and len(form_output) > 0:
                response = form_output[-1].content
            else:
                response = "Unable to analyze form"
            
            result = {
                "form_analysis": response,
                "exercise": exercise,
                "status": "success"
            }
            
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@gym_trainer_bp.route('/health', methods=['GET'])
def gym_trainer_health_check():
    """Health check endpoint for Gym Trainer"""
    try:
        gym_trainer = create_gym_trainer_agent()
        
        status = "healthy" if gym_trainer else "unhealthy"
        return jsonify({
            "status": status, 
            "service": "gym_trainer",
            "agent_available": gym_trainer is not None
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "service": "gym_trainer",
            "error": str(e)
        }), 500 
