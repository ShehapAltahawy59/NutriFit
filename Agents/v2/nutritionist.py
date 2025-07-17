from collections import defaultdict
import json
from fastapi import APIRouter, Request
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_core.models import UserMessage
from autogen_core import Image as AGImage
from PIL import Image
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from io import BytesIO
import requests
import asyncio
from pydantic import BaseModel
from typing import Dict, List, Optional

from Agents.v2.gym_trainer import process_inbody_image
from . import initialize_azure_client

# Create APIRouter for Nutritionist
router = APIRouter()

# Pydantic models for nutrition planning
class IngredientAlternative(BaseModel):
    name: str
    quantity: str 
# Pydantic models for nutrition planning
class Ingredient(BaseModel):
    name: str  # Can be in any language
    quantity: str
    alternatives: IngredientAlternative  # Still language-flexible


class DayPlan(BaseModel):
    week: str  # e.g., "Week 1", "الأسبوع الأول"
    day: str   # e.g., "Monday", "الإثنين"
    meal_type: str # e.g. "breakfast", "lunch", "عشاء"
    ingredients: List[Ingredient]


class FourWeekDietPlan(BaseModel):
    plan: List[DayPlan]  # 28 items: 4 weeks * 7 days



# ----------------------------
# 🔁 Convert Flat → Nested
# ----------------------------

def convert_flat_to_nested(nutrition_result):
    result = {"plan": []}
    plan_entries = nutrition_result["plan"]

    week_map = {}

    # Arabic to English meal type map
    

    meal_map = {
        "فطور": "breakfast",
        "غداء": "lunch",
        "عشاء": "dinner",
        "وجبة خفيفة": "snack"
    }

    for entry in plan_entries:
        week = entry["week"]
        day = entry["day"]
        meal_type = meal_map.get(entry["meal_type"], entry["meal_type"])

        # Create week if not exists
        if week not in week_map:
            week_obj = {"week": week, "days": []}
            week_map[week] = week_obj
            result["plan"].append(week_obj)

        week_obj = week_map[week]

        # Check if day already added
        day_obj = next((d for d in week_obj["days"] if d["day"] == day), None)
        if not day_obj:
            day_obj = {"day": day, "meals": {}}
            week_obj["days"].append(day_obj)

        # Add meal items
        ingredients = entry.get("ingredients", [])
        meal_items = []
        for item in ingredients:
            meal_items.append({
                "name": item.get("name", ""),
                "quantity": item.get("quantity", ""),
                "alternatives": {
                    "name": item.get("alternatives", {}).get("name", ""),
                    "quantity": item.get("alternatives", {}).get("quantity", "")
                }
            })

        day_obj["meals"][meal_type] = meal_items

    return result
    


def create_nutritionist_agent():
    """Create and return the main Nutritionist agent"""
    client = initialize_azure_client()
    if not client:
        return None
    
    nutritionist = AssistantAgent(
        name="nutritionist",
        model_client=client,
        system_message = f"""
        You are a certified professional nutritionist.
        Based on user history nutritionPlan, current user's InBody report image,the user calories needed,number of gym days,Goal ,Country and allergies generate a complete 4-week diet plan for the client:
        Provide a 4-week meal plan, with a different meal for each day. Each week must include 7 days, and every day must include breakfast, lunch, snack, and dinner.
        Meals should be simple, practical, and easy to prepare, with clear ingredients and quantities.
        Each meal should have main ingredients and one Ingredient Alternative.
        Meals should reflect ingredients commonly available in client country.
        ingredients must be  clearly listed with understandable quantities (grams or pieces only) for all days in all weeks
        Units of measurement should also be used and known in client country.
        Main Note: Don't include any foods or ingredients the client is allergic to.
        Do not include any explanation, recommendations, or analysis — only provide the structured 4-week diet plan in a clean and clear format.
        return the response with the language the user give to you.
        """,
      output_content_type= FourWeekDietPlan
   )
    
    return nutritionist

def create_evaluator_agent():
    """Create and return the Evaluator agent"""
    client = initialize_azure_client()
    if not client:
        return None
    
    evaluator = AssistantAgent(
        name="evaluator",
        model_client=client,
        system_message=f"""
        You are a certified nutritionist and evaluator.
        You will assess a 4-week diet plan based on the client's calories,number of gym days, allergies, cultural context, and health goal.

        You must evaluate the following (critical):
        1. Goal Alignment: Does the plan help the client lose weight and build muscle?
        2. Allergen Safety: Is the plan 100% free from all foods containing or made with user allergies?
        3. Cultural Relevance: Are the ingredients, meals, and units common and understandable in user country?
        4. Nutritional Balance: Are meals rich in protein, fiber, and healthy fats while being moderate in calories?
        5. Meal Variety: Is there enough variety in meals across all 4 weeks to avoid repetition?
        6. Clarity & Portion Consistency (It is very criticall): Are ingredients clearly listed with understandable quantities (cups, grams, pieces, etc.) for all days in all weeks?
        
        Instructions:
        - Read the full plan.
        - Suggest specific improvements only if it is critical.
        - if there is no need for improvements, just output "approved"

        Do NOT include any unrelated explanations or code. Keep output clear, evaluative, and well-formatted.
        """,
        
    )
    
    return evaluator

def create_nutrition_team(nutritionist, evaluator):
    """Create a team chat for nutrition planning"""
    text_termination = TextMentionTermination(
        "approved"
    )
    
    team = RoundRobinGroupChat(
        [nutritionist, evaluator], 
        termination_condition=text_termination, 
        max_turns=6
    )
    
    return team

async def process_food_image(image_url):
    """Process and analyze food image if provided"""
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
        print(f"Error processing food image: {e}")
        return None

async def create_comprehensive_nutrition_plan(language,inbody_data,calories,number_of_gym_days,client_country, goals, allergies,last_nutritionPlan,last_plan_inbody_data):
    """Create a comprehensive nutrition plan using nutritionist and evaluator team"""
    try:
        # Initialize agents
        nutritionist = create_nutritionist_agent()
        evaluator = create_evaluator_agent()
        
        if not nutritionist or not evaluator:
            return {"error": "Failed to initialize nutrition agents"}
        
        # Process image if provided
        #image = await process_food_image(image_url)
        
        # Create team chat
        team = create_nutrition_team(nutritionist, evaluator)
        
        # Prepare user message based on meal plan type
   
        if last_nutritionPlan:
            last_nutritionPlan = last_nutritionPlan
        else:
            last_nutritionPlan="no history for that user"
        user_message = f"""
        last_nutritionPlan:{last_nutritionPlan}
        last inbody data:{last_plan_inbody_data}
        current inbody data:{inbody_data}
        calories:{calories},
        number_of_gym_days:{number_of_gym_days},
        Client Country: {client_country}
        Goals: {goals}
        Allergies: {allergies}
        language:{language}
        Please create a comprehensive 4-week nutrition plan based on this data.
        """
        
        # Create message
        
        message = MultiModalMessage(content=[user_message],source="User")
        # Get nutrition plan from team
        diet_plan_output = await team.run(task=message)
        
        # Extract the response
        if diet_plan_output :
            response = diet_plan_output.messages[-2].content
            if hasattr(response, "model_dump"):
                response_dict = response.model_dump()
            else:
                response_dict = response.dict()
            response = convert_flat_to_nested(response_dict)
            
        else:
            response = "Unable to generate nutrition plan"
        
        return {
            "diet_plan": response,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": f"Error creating nutrition plan: {str(e)}",
            "status": "error"
        }



# Flask routes for Nutritionist
@router.post('/create_plan')
async def create_nutrition_plan(request: Request):
    """Main endpoint for creating comprehensive nutrition plans"""
    try:
        data = await request.json()
        
        # Validate input
        if not data:
            return {"error": "No data provided"}
        
        required_fields = ['inbody_image_url', 'goals', 'allergies']
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}
        
        # Extract data
        inbody_image_url = data['inbody_image_url']
        calories = data['calories']
        goals = data['goals']
        allergies = data['allergies']
        number_of_gym_days = data['number_of_gym_days']
        client_country = data["client_country"]

        
        # Create nutrition plan
        result = await create_comprehensive_nutrition_plan(inbody_image_url,calories,number_of_gym_days,client_country, goals, allergies)
        
        return result
        
    except Exception as e:
        return {"error": f"Server error: {str(e)}"}



