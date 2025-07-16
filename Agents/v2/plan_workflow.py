"""
Plan Workflow - Complete Nutrition Planning Pipeline

This module orchestrates the complete workflow from InBody image analysis
to nutrition plan generation using all three agents:
1. InBody Specialist - Analyzes body composition from image
2. Nutritionist - Creates 4-week diet plan based on analysis
3. Evaluator - Validates the plan

The workflow processes:
- InBody scan image
- Client country for cultural relevance
- Health goals
- Allergies and restrictions
"""

import asyncio
import json
from flask import Blueprint, request, jsonify
from pydantic import BaseModel
from typing import Optional
import requests
from PIL import Image
from io import BytesIO
from flask_cors import cross_origin

# Import agent functions
from .inbody_specialist import create_inbody_agent, process_inbody_analysis, process_inbody_image
from .nutritionist import create_comprehensive_nutrition_plan, create_nutritionist_agent, create_evaluator_agent, create_nutrition_team
from autogen_core import CancellationToken
from autogen_core.models import UserMessage
from autogen_agentchat.messages import MultiModalMessage
from .gym_trainer import create_comprehensive_workout_plan
from Agents.firebase_plans import get_user_plans, increment_used_requests, save_full_user_plan, send_plan_created_notification
from .summerizer import summerize_workout_plan

# Create Blueprint for Plan Workflow
workflow_bp = Blueprint('plan_workflow_v2', __name__)

# Pydantic models for workflow
class WorkflowRequest(BaseModel):
    inbody_image_url: str
    client_country: str
    goals: str
    allergies: str = ""
    user_info: Optional[str] = ""

class WorkflowResponse(BaseModel):
    inbody_analysis: dict
    nutrition_plan: dict
    status: str
    workflow_steps: list

class WorkflowStep(BaseModel):
    step: str
    status: str
    message: str
    data: Optional[dict] = None




async def execute_complete_workflow(
    inbody_image_url: str,
    client_country: str,
    goals: str,
    allergies: str = "",
    injuries: str = "",
    number_of_gym_days: str = "",
    user_id: str = None,
    language:str = "english",
    time:str = "",
    type:str = ""
) -> dict:
    """
    Execute the complete workflow: (history summary) -> InBody image -> gym plan -> nutrition plan
    """
    image = await process_inbody_image(inbody_image_url)
    if not image:
            return {
                "error": "Failed to process InBody image",
                "status": "error"
            }
    workflow_steps = []
    try:
        # Step 0: Fetch and summarize last plan if exists
        last_plan_summary = ""
        last_plan_inbody_data=""
        if user_id:
            last_plan = get_user_plans(user_id)
            if last_plan:
               
                plan_to_summarize = {
                    'gymPlan': last_plan.get('gymPlan'),
                    'nutritionPlan': last_plan.get('nutritionPlan')
                }
                summary_result = await summerize_workout_plan(plan_to_summarize)
                last_plan_summary = summary_result.get('summerizer_output')
                last_plan_inbody_data=last_plan.get('inbody_data',"")
        workflow_steps.append(WorkflowStep(
            step="history_summary",
            status="completed" if last_plan_summary else "skipped",
            message="Summarized last user plan" if last_plan_summary else "No previous plan found to summarize",
            data={"summary": last_plan_summary} if last_plan_summary else None
        ))
        # 1: InBody Analysis
        workflow_steps.append(WorkflowStep(
            step="inbody_analysis",
            status="processing",
            message="Processing InBody image and extracting body composition data"
        ))
        inbody_result = await process_inbody_analysis(image)
        if inbody_result["status"] == "error":
            workflow_steps[-1].status = "failed"
            workflow_steps[-1].message = inbody_result.get("error", "InBody analysis failed")
            return {
                "message": "Workflow failed at InBody analysis step",
                "workflow_steps": [step.dict() for step in workflow_steps],
                "status": "error"
            }
        if (inbody_result["analysis"]["status"] == "not valid image"):
            workflow_steps[-1].status = "failed"
            workflow_steps[-1].message = inbody_result.get("error", "InBody analysis failed")
            return {
                "message": "failed as the image is not InBody analysis",
                "status": "error"
            }
        workflow_steps[-1].status = "completed"
        workflow_steps[-1].message = "InBody analysis completed successfully"
        workflow_steps[-1].data = {"analysis": inbody_result["analysis"]}
        inbody_data=inbody_result["analysis"]["results"]
        gym_result=None
        calories = ""

        if int(number_of_gym_days) > 0:
            # Step 2: Gym Plan Creation
            workflow_steps.append(WorkflowStep(
                step="gym_plan_creation",
                status="processing",
                message="Creating comprehensive gym plan"
            ))
            gym_result = await create_comprehensive_workout_plan(
                inbody_data,
                injuries,
                goals,
                number_of_gym_days,
                last_plan_summary,
                last_plan_inbody_data,
                type
                
            )
            if gym_result["status"] == "error":
                workflow_steps[-1].status = "failed"
                workflow_steps[-1].message = gym_result.get("error", "Gym plan creation failed")
                return {
                    "message": "Workflow failed at gym plan creation step",
                    "workflow_steps": [step.dict() for step in workflow_steps],
                    "status": "error"
                }
            workflow_steps[-1].status = "completed"
            workflow_steps[-1].message = "Gym plan created successfully"
            workflow_steps[-1].data = {"gym_plan": gym_result["workout_plan"]}

        # Extract calories from gym plan
            
            plan = gym_result["workout_plan"]
            if hasattr(plan, "daily_calories"):
                calories = plan.daily_calories
            elif isinstance(plan, dict) and "daily_calories" in plan:
                calories = plan["daily_calories"]

        # Step 3: Nutrition Plan Creation
        workflow_steps.append(WorkflowStep(
            step="nutrition_planning",
            status="processing",
            message="Creating comprehensive nutrition plan with evaluation"
        ))
        nutrition_result = await create_comprehensive_nutrition_plan(
            language,
            inbody_data,
            calories ,
            number_of_gym_days,
            client_country,
            goals,
            allergies,
            last_plan_summary,
            last_plan_inbody_data
        )
        if nutrition_result["status"] == "error":
            workflow_steps[-1].status = "failed"
            workflow_steps[-1].message = nutrition_result.get("error", "Nutrition planning failed")
            return {
                "message": "Workflow failed at nutrition planning step",
                "workflow_steps": [step.dict() for step in workflow_steps],
                "status": "error"
            }
        workflow_steps[-1].status = "completed"
        workflow_steps[-1].message = "Nutrition plan created and evaluated successfully"
        workflow_steps[-1].data = {"diet_plan": nutrition_result["diet_plan"]}

        # Step 4: Workflow Completion
        workflow_steps.append(WorkflowStep(
            step="workflow_completion",
            status="completed",
            message="Complete workflow finished successfully"
        ))
        # Save plan to DB if user_id is provided
        if user_id:
            try:
                save_full_user_plan(
                    user_id=user_id,
                    gym_plan=gym_result["workout_plan"] if gym_result else {},
                    nutrition_plan=nutrition_result["diet_plan"],
                    image_url=inbody_image_url,
                    is_viewed=False,
                    subscription_type=0,
                    time=time,
                    inbody_data=inbody_data
                )
                increment_used_requests(user_id)
                send_plan_created_notification(user_id)
            except Exception as e:
                # Optionally log or append to workflow_steps
                workflow_steps.append(WorkflowStep(
                    step="db_save",
                    status="failed",
                    message=f"Failed to save plan to DB: {str(e)}"
                ))
        return {
            "nutrition_result":nutrition_result,
            "status": "success"
        }
    except Exception as e:
        workflow_steps.append(WorkflowStep(
            step="workflow_error",
            status="failed",
            message=f"Workflow failed with error: {str(e)}"
        ))
        return {
            "message": f"Workflow execution failed: {str(e)}",
            "workflow_steps": [step.dict() for step in workflow_steps],
            "status": "error"
        }

# Flask routes for Plan Workflow
@workflow_bp.route('/create_complete_plan', methods=['POST'])
@cross_origin()
def create_complete_plan():
    """Main endpoint for complete nutrition and gym planning workflow"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        required_fields = ['type','time','user_id','inbody_image_url', 'client_country', 'goals', 'injuries', 'number_of_gym_days']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        inbody_image_url = data['inbody_image_url']
        client_country = data['client_country']
        goals = data['goals']
        allergies = data.get('allergies', '')
        injuries = data['injuries']
        number_of_gym_days = data['number_of_gym_days']
        user_id = data.get('user_id', None)
        language = data.get('lang', "english")
        time=data['time']
        type=data['type']
        # Validate image URL
        try:
            response = requests.head(inbody_image_url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            return jsonify({"error": f"Invalid or inaccessible image URL: {str(e)}"}), 400
       
        
        result = asyncio.run(
            execute_complete_workflow(
                
                inbody_image_url,
                client_country,
                goals,
                allergies,
                injuries,
                number_of_gym_days,
                user_id,
                language,
                time,
                type
            )
        )
        
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@workflow_bp.route('/workflow_status', methods=['GET'])
@cross_origin()
def workflow_status():
    """Get workflow status and capabilities"""
    try:
        # Check if all required agents are available
        inbody_agent = create_inbody_agent()
        nutritionist_agent = create_nutritionist_agent()
        evaluator_agent = create_evaluator_agent()
        
        all_agents_available = all([inbody_agent, nutritionist_agent, evaluator_agent])
        
        return jsonify({
            "workflow_status": "ready" if all_agents_available else "unavailable",
            "agents": {
                "inbody_specialist": "available" if inbody_agent else "unavailable",
                "nutritionist": "available" if nutritionist_agent else "unavailable",
                "evaluator": "available" if evaluator_agent else "unavailable"
            },
            "workflow_steps": [
                "InBody image analysis and data extraction",
                "Nutrition plan creation with cultural adaptation",
                "Plan evaluation and validation"
            ],
            "required_inputs": [
                "inbody_image_url (required)",
                "client_country (required)",
                "goals (required)",
                "allergies (optional)",
                "user_info (optional)"
            ]
        })
        
    except Exception as e:
        return jsonify({
            "workflow_status": "error",
            "error": f"Error checking workflow status: {str(e)}"
        }), 500


@workflow_bp.route('/health', methods=['GET'])
@cross_origin()
def workflow_health_check():
    """Health check endpoint for Plan Workflow"""
    try:
        # Check all required agents
        inbody_agent = create_inbody_agent()
        nutritionist_agent = create_nutritionist_agent()
        evaluator_agent = create_evaluator_agent()
        
        all_agents_available = all([inbody_agent, nutritionist_agent, evaluator_agent])
        
        return jsonify({
            "status": "healthy" if all_agents_available else "unhealthy",
            "service": "plan_workflow",
            "agents_available": all_agents_available,
            "workflow_ready": all_agents_available
        })
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "service": "plan_workflow",
            "error": str(e)
        }), 500 
