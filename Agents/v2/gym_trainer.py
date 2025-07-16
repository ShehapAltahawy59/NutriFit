import json
from fastapi import APIRouter, Request
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
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
# Create APIRouter for Gym Trainer
router = APIRouter()

# Pydantic models for fitness training
class Exercise(BaseModel):
    name: str
    sets: int
    reps: str  # string to allow formats like "30 sec", "10 reps per leg", etc.
    rest: str  # string to allow formats like "30 sec", "60 sec", etc.

class DailyWorkout(BaseModel):
    day: str
    exercises: List[Exercise]

class GymTrainingPlan(BaseModel):
    weekly_plan: List[DailyWorkout]
    daily_calories: int

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


async def process_inbody_image(image_url):
    """Process and analyze InBody scan image if provided"""
    if not image_url:
        return None
    
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Convert to PIL Image
        image = Image.open(BytesIO(response.content))
        
        # Convert to AutoGen Image format
        ag_image = AGImage(image)
        
        return ag_image
    except Exception as e:
        print(f"Error processing InBody image: {e}")
        return None


def create_gym_trainer_agent():
    """Create and return the Gym Trainer agent"""
    client = initialize_azure_client()
    if not client:
        return None
    gym_system_message = f"""
                            You are a certified professional Gym Trainer.
                            Based on the user history (gymPlan & inbody data),current user's InBody report data, goal, sex, injuries, and number of gym days, generate a gym training plan for the client.
                            Provide a gym training plan for one week, with a different workout for each day and in each day write the focus in the day for example (leg day).
                            The plan should include exercises, sets, reps, and rest times.
                            Ensure the plan is suitable for the client's goal.
                            Use the most famous gym machines in the workout plan.
                            Based on the goal, InBody data, and training plan, you should also output the number of calories to be consumed daily.
                            Rule:based on the user workout type(home,gym) you will give him plan sutible for that.
                            Note: number of excercises should be 4-8 exercises per day.
                            Main Note: Do not include any exercises that may aggravate the client's injuries.
                            Do not include any explanation, analysis, recommendations, or client headers (like name, goal, age, gender, etc).
                            Only output the clean structured weekly plan and calories in English.
                            Output in English.
                            """
    GymTrainer = AssistantAgent(
    name="GymTrainer_agent",
    model_client=client,
    system_message =gym_system_message,
    output_content_type= GymTrainingPlan
    )
    
    return GymTrainer


def create_gym_evalutor_agent():
    """Create and return the Gym Trainer agent"""
    client = initialize_azure_client()
    if not client:
        return None
    GymTrainer_evaluator_system_message = f"""
            You are a certified nutritionist and evaluator.
            You will assess a one week workout plan based on the client's body composition analysis, sex, injuries, goal and number of gym days.
            You must evaluate the workout (critical):
            1. Goal Alignment: Does the plan help the client achieve their goal ?
            2. Injury Safety: Are all exercises safe for the client's injuries?
            3. Exercise Variety: Are there enough different exercises to keep the client engaged?
            4. Does the plan include all muscles and without repition of exercises and days focus in the week?
            Instructions:
            - Read the full plan.
            - Suggest specific improvements only if it is critical.
            - if there is no need for improvements, just output "approved"

            Do NOT include any unrelated explanations or code. Keep output clear, evaluative, and well-formatted.
            """

    GymTrainer_evaluator = AssistantAgent(
        name="evaluator_agent",
        model_client=client,
        system_message=GymTrainer_evaluator_system_message
    )
    
    return GymTrainer_evaluator


async def create_comprehensive_workout_plan(inbody_data, injuries, goals, number_of_gym_days,lastgymPlan,last_plan_inbody_data,type):
    """Create a comprehensive workout plan"""
    try:
        # Initialize Gym Trainer agent
        gym_trainer = create_gym_trainer_agent()
        gym_evaluator = create_gym_evalutor_agent()

        if not gym_trainer or not gym_evaluator:
            return {"error": "Failed to initialize Gym Trainer agent"}
        
        
        
        # Prepare workout plan message
        text_termination = TextMentionTermination("approved")
    
        
        gym_team = RoundRobinGroupChat([gym_trainer, gym_evaluator], termination_condition=text_termination, max_turns=6)
        if lastgymPlan:
            lastgymPlan = lastgymPlan
        else:
            lastgymPlan="no history for that user"
        
        user_message = f"""
        last gym Plan:{lastgymPlan}
        last inbody data:{last_plan_inbody_data}
        current inbody data:{inbody_data}
        Goals: {goals}
        injuries: {injuries}
        number of gym days: {number_of_gym_days},
        workout type:{type}
        """
        message = MultiModalMessage(content=[user_message],source="User")

        workout_plan_output = await gym_team.run(task=message)
        workout_output = workout_plan_output.messages[-2].content
        # Extract the response
        if workout_output:
            response = workout_output
            # Convert Pydantic model (or any nested models) to dict
            if hasattr(response, "model_dump"):
                response = response.model_dump()
            elif hasattr(response, "dict"):
                response = response.dict()
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
@router.post('/create_workout')
async def create_workout_plan(request: Request):
    """Main endpoint for creating comprehensive workout plans"""
    try:
        data = await request.json()
        
        # Validate input
        if not data:
            return {"error": "No data provided"}, 400
        
        required_fields = ['inbody_image_url', 'injuries', 'goals', 'number_of_gym_days']
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}, 400
        
        # Extract data
        image_url = data['inbody_image_url']
        injuries = data['injuries']
        goals = data['goals']
        number_of_gym_days = data['number_of_gym_days']
        
        
        # Create workout plan
        result = await create_comprehensive_workout_plan(image_url, injuries, goals,number_of_gym_days)
        
        return result
        
    except Exception as e:
        return {"error": f"Server error: {str(e)}"}, 500


