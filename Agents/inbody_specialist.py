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
from typing import Optional
from . import initialize_azure_client

# Create Blueprint for Inbody Specialist
inbody_bp = Blueprint('inbody_specialist', __name__)

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
    "perform the following tasks: Extract all measurable data from the image." \
    "Ensure accuracy in all extracted values, as all numbers and metrics are critical." \
    "Present the extracted data in a well-structured and labeled format, without any analysis or recommendations or any other text." \
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

async def analyze_inbody_data(user_info, scan_data="", image_url="", goals=""):
    """Analyze InBody data and provide comprehensive insights"""
    try:
        # Initialize Inbody Specialist agent
        inbody_agent = create_inbody_agent()
        
        if not inbody_agent:
            return {"error": "Failed to initialize Inbody Specialist agent"}
        
        # Process image if provided
        image = await process_inbody_image(image_url)
        
        # Prepare analysis message
        analysis_message = f"""
        User Information: {user_info}
        Goals: {goals}
        
        InBody Scan Data: {scan_data}
        
        Please provide a comprehensive analysis of the body composition data, including:
        1. Body composition breakdown (muscle mass, fat mass, water content)
        2. Metabolic health indicators
        3. Specific recommendations for improvement
        4. Progress tracking guidance
        5. Risk factors and areas of concern
        6. Personalized advice based on the user's goals
        """
        
        # Create multimodal message with image
        message = MultiModalMessage(content=[analysis_message, image], source="User")
        
        # Get analysis from Inbody Specialist
        analysis_output = await inbody_agent.on_messages(
            message, 
            cancellation_token=CancellationToken()
        )
        
        # Extract the response
        if analysis_output and len(analysis_output) > 0:
            response = analysis_output[-1].content
        else:
            response = "Unable to generate InBody analysis"
        
        return {
            "analysis": response,
            "recommendations": "Analysis completed successfully",
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": f"Error analyzing InBody data: {str(e)}",
            "status": "error"
        }

# Flask routes for Inbody Specialist
@inbody_bp.route('/analyze', methods=['POST'])
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
                analyze_inbody_data(user_info, scan_data, image_url, goals)
            )
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@inbody_bp.route('/health', methods=['GET'])
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
