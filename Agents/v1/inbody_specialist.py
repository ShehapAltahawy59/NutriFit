from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
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
from typing import Optional
from .. import initialize_azure_client

# Create Blueprint for Inbody Specialist
inbody_bp = Blueprint('inbody_specialist_v1', __name__)

# Pydantic models for Inbody analysis
class InbodyAnalysisRequest(BaseModel):
    user_info: str
    scan_data: Optional[str] = ""
    image_url: Optional[str] = ""
    goals: Optional[str] = ""

class InbodyAnalysisResponse(BaseModel):
    analysis: dict
    recommendations: str
    status: str

def create_inbody_agent():
    """Create and return the Inbody Specialist agent"""
    client = initialize_azure_client()
    if not client:
        return None
    
    Inbody_Specialist = AssistantAgent(
    name="Inbody_Speciallist_agent",
    model_client=client,
    system_message="You are a professional Inbody Speciallist. I will upload an InBody analysis report image." \
    "you check if the image is InBody analysis report or not "
    "Rule:if the image is not InBody analysis report return  'not valid image' "
    "Rule:if the image is  InBody analysis report return  'valid image' "
    "note: make the output text "
    )
    
    return Inbody_Specialist

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
        Please check if this image is InBody analysis report or not
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
# Flask routes for Inbody Specialist
@inbody_bp.route('/analyze', methods=['POST'])
@cross_origin()
def analyze_inbody():
    """Main endpoint for InBody analysis"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if 'user_info' not in data:
            return jsonify({"error": "Missing required field: user_info"}), 400
        
        # Extract data
        user_info = data['user_info']
        scan_data = data.get('scan_data', '')
        image_url = data.get('image_url', '')
        goals = data.get('goals', '')
        
        # Perform InBody analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                process_inbody_analysis(user_info, scan_data, image_url, goals)
            )
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@inbody_bp.route('/health', methods=['GET'])
@cross_origin()
def inbody_health_check():
    """Health check endpoint for Inbody Specialist"""
    try:
        agent = create_inbody_agent()
        status = "healthy" if agent else "unhealthy"
        return jsonify({
            "status": status, 
            "service": "inbody_specialist",
            "agent_available": agent is not None
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "service": "inbody_specialist",
            "error": str(e)
        }), 500

@inbody_bp.route('/simple_analysis', methods=['POST'])
@cross_origin()
def simple_inbody_analysis():
    """Simplified endpoint for basic InBody analysis"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({"error": "Query is required"}), 400
        
        query = data['query']
        
        # Initialize Inbody Specialist agent
        inbody_agent = create_inbody_agent()
        
        if not inbody_agent:
            return jsonify({"error": "Failed to initialize Inbody Specialist agent"}), 500
        
        # Create simple response
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            response = loop.run_until_complete(
                inbody_agent.on_messages(
                    UserMessage(content=query),
                    cancellation_token=CancellationToken()
                )
            )
        finally:
            loop.close()
        
        if response and len(response) > 0:
            result = response[-1].content
        else:
            result = "Unable to generate response"
        
        return jsonify({"response": result, "status": "success"})
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500 
