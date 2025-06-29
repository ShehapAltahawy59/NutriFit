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
from flask import Blueprint, request, jsonify
from pydantic import BaseModel
from typing import Optional
import requests
from PIL import Image
from io import BytesIO
from flask_cors import cross_origin

# Import agent functions
from .inbody_specialist import create_inbody_agent, process_inbody_image
from .nutritionist import create_nutritionist_agent, create_evaluator_agent, create_nutrition_team
from autogen_core import CancellationToken
from autogen_core.models import UserMessage
from autogen_agentchat.messages import MultiModalMessage

# Create Blueprint for Plan Workflow
workflow_bp = Blueprint('plan_workflow', __name__)

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

async def process_inbody_analysis(image_url: str, user_info: str = "", goals: str = "") -> dict:
    """
    Step 1: Process InBody image and extract body composition data
    
    Args:
        image_url: URL of the InBody scan image
        user_info: Additional user information
        goals: User's health goals
    
    Returns:
        dict: InBody analysis results
    """
    try:
        # Initialize InBody Specialist agent
        inbody_agent = create_inbody_agent()
        
        if not inbody_agent:
            return {
                "error": "Failed to initialize InBody Specialist agent",
                "status": "error"
            }
        
        # Process InBody image
        image = await process_inbody_image(image_url)
        
        if not image:
            return {
                "error": "Failed to process InBody image",
                "status": "error"
            }
        
        # Prepare analysis message
        analysis_message = f"""
        Please extract all measurable data from this InBody analysis report image.
        """
        
        # Create multimodal message with image
        message = MultiModalMessage(content=[image],source="User")
        
        # Get analysis from InBody Specialist
        analysis_output = await inbody_agent.on_messages(
            [message], 
            cancellation_token=CancellationToken()
        )
        
        # Extract the response
        if analysis_output :
            response = analysis_output.chat_message.content
        else:
            response = "Unable to generate InBody analysis"
        
        return {
            "analysis": response,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": f"Error in InBody analysis: {str(e)}",
            "status": "error"
        }

async def create_nutrition_plan_with_evaluation(
    inbody_analysis: str, 
    client_country: str, 
    goals: str, 
    allergies: str
) -> dict:
    """
    Step 2: Create nutrition plan using nutritionist and evaluator team
    
    Args:
        inbody_analysis: Results from InBody analysis
        client_country: Client's country for cultural relevance
        goals: User's health goals
        allergies: User's allergies and restrictions
    
    Returns:
        dict: Nutrition plan with evaluation
    """
    try:
        # Initialize agents
        nutritionist = create_nutritionist_agent()
        evaluator = create_evaluator_agent()
        
        if not nutritionist or not evaluator:
            return {
                "error": "Failed to initialize nutrition agents",
                "status": "error"
            }
        
        # Create team chat
        team = create_nutrition_team(nutritionist, evaluator)
        
        # Prepare user message
        user_message = f"""
        Report data: {inbody_analysis}
        Client Country: {client_country}
        Goals: {goals}
        Allergies: {allergies}
        Please create a comprehensive 4-week nutrition plan based on this data.
        """
        
        # Create message
        message = UserMessage(content=[user_message],source="User")
        
        # Get nutrition plan from team
        diet_plan_output = await team.run(task=user_message)
        
        # Extract the response
        if diet_plan_output :
            response = diet_plan_output.messages[-2].content.plan
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

async def execute_complete_workflow(
    inbody_image_url: str,
    client_country: str,
    goals: str,
    allergies: str = "",
    user_info: str = ""
) -> dict:
    """
    Execute the complete workflow from InBody image to nutrition plan
    
    Args:
        inbody_image_url: URL of the InBody scan image
        client_country: Client's country for cultural relevance
        goals: User's health goals
        allergies: User's allergies and restrictions
        user_info: Additional user information
    
    Returns:
        dict: Complete workflow results
    """
    workflow_steps = []
    
    try:
        # Step 1: InBody Analysis
        workflow_steps.append(WorkflowStep(
            step="inbody_analysis",
            status="processing",
            message="Processing InBody image and extracting body composition data"
        ))
        
        inbody_result = await process_inbody_analysis(inbody_image_url, user_info, goals)
        
        if inbody_result["status"] == "error":
            workflow_steps[-1].status = "failed"
            workflow_steps[-1].message = inbody_result.get("error", "InBody analysis failed")
            return {
                "error": "Workflow failed at InBody analysis step",
                "workflow_steps": [step.dict() for step in workflow_steps],
                "status": "error"
            }
        
        workflow_steps[-1].status = "completed"
        workflow_steps[-1].message = "InBody analysis completed successfully"
        workflow_steps[-1].data = {"analysis": inbody_result["analysis"]}
        
        # Step 2: Nutrition Plan Creation
        workflow_steps.append(WorkflowStep(
            step="nutrition_planning",
            status="processing",
            message="Creating comprehensive nutrition plan with evaluation"
        ))
        
        nutrition_result = await create_nutrition_plan_with_evaluation(
            inbody_result["analysis"],
            client_country,
            goals,
            allergies
        )
        
        if nutrition_result["status"] == "error":
            workflow_steps[-1].status = "failed"
            workflow_steps[-1].message = nutrition_result.get("error", "Nutrition planning failed")
            return {
                "error": "Workflow failed at nutrition planning step",
                "workflow_steps": [step.dict() for step in workflow_steps],
                "status": "error"
            }
        
        workflow_steps[-1].status = "completed"
        workflow_steps[-1].message = "Nutrition plan created and evaluated successfully"
        workflow_steps[-1].data = {"diet_plan": nutrition_result["diet_plan"]}
        
        # Step 3: Workflow Completion
        workflow_steps.append(WorkflowStep(
            step="workflow_completion",
            status="completed",
            message="Complete nutrition planning workflow finished successfully"
        ))
        
        return {
            "inbody_analysis": inbody_result["analysis"],
            "nutrition_plan": nutrition_result["diet_plan"],
            "workflow_steps": [step.dict() for step in workflow_steps],
            "status": "success"
        }
        
    except Exception as e:
        # Add error step if workflow fails
        workflow_steps.append(WorkflowStep(
            step="workflow_error",
            status="failed",
            message=f"Workflow failed with error: {str(e)}"
        ))
        
        return {
            "error": f"Workflow execution failed: {str(e)}",
            "workflow_steps": [step.dict() for step in workflow_steps],
            "status": "error"
        }

# Flask routes for Plan Workflow
@workflow_bp.route('/create_complete_plan', methods=['POST'])
@cross_origin()
def create_complete_plan():
    """Main endpoint for complete nutrition planning workflow"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['inbody_image_url', 'client_country', 'goals']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Extract data
        inbody_image_url = data['inbody_image_url']
        client_country = data['client_country']
        goals = data['goals']
        allergies = data.get('allergies', '')
        user_info = data.get('user_info', '')
        
        # Validate image URL
        try:
            response = requests.head(inbody_image_url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            return jsonify({"error": f"Invalid or inaccessible image URL: {str(e)}"}), 400
        
        # Execute complete workflow
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                execute_complete_workflow(
                    inbody_image_url,
                    client_country,
                    goals,
                    allergies,
                    user_info
                )
            )
        finally:
            loop.close()
        
        diet_plan_dict = [week.model_dump() for week in result["nutrition_plan"]]
        return jsonify(diet_plan_dict)
        
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

@workflow_bp.route('/test_inbody_analysis', methods=['POST'])
@cross_origin()
def test_inbody_analysis():
    """Test endpoint for InBody analysis only"""
    try:
        data = request.get_json()
        
        if not data or 'inbody_image_url' not in data:
            return jsonify({"error": "inbody_image_url is required"}), 400
        
        inbody_image_url = data['inbody_image_url']
        user_info = data.get('user_info', '')
        goals = data.get('goals', '')
        
        # Execute InBody analysis only
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                process_inbody_analysis(inbody_image_url, user_info, goals)
            )
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

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
