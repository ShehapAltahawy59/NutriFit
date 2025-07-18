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
from typing import Optional
from . import initialize_azure_client
from pydantic import BaseModel, Field
# Create APIRouter for Inbody Specialist
router = APIRouter()

# Pydantic models for Inbody analysis
from pydantic import BaseModel
from typing import Optional, Dict


class InbodyData(BaseModel):
    gendeer: Optional[str] = Field(None, description="Gender")
    weight: Optional[float] = Field(None, description="Weight in kilograms")
    height: Optional[float] = Field(None, description="Height in centimeters")
    body_fat_percentage: Optional[float] = Field(None, description="Body fat percentage")
    body_fat_mass: Optional[float] = Field(None, description="Body fat mass in kilograms")
    muscle_mass: Optional[float] = Field(None, description="Skeletal muscle mass")
    fat_free_mass: Optional[float] = Field(None, description="Fat-free mass in kilograms")
    bmi: Optional[float] = Field(None, description="Body Mass Index")
    basal_metabolic_rate: Optional[float] = Field(None, description="Basal Metabolic Rate in kcal")
    metabolic_age: Optional[int] = Field(None, description="Metabolic age")
    protein: Optional[float] = Field(None, description="Protein level")
    minerals: Optional[float] = Field(None, description="Mineral content")
    body_water: Optional[float] = Field(None, description="Total body water")
    visceral_fat_level: Optional[float] = Field(None, description="Visceral fat level")
    waist_hip_ratio: Optional[float] = Field(None, description="Waist-Hip Ratio")
    obesity_degree: Optional[float] = Field(None, description="Obesity Degree")
    segmental_fat: Optional[str] = Field(None, description="Segmental fat info")
    segmental_muscle: Optional[str] = Field(None, description="Segmental muscle info")
    impedance: Optional[Dict[str, float]] = Field(None, description="Impedance values by body part")
    inbody_score: Optional[int] = Field(None, description="Overall InBody score")


class ImageResponse(BaseModel):
    status: str  # either "ok" or "not valid image"
    results: Optional[InbodyData] = {}  # Only present if status is "ok"
    


# Final Union Output


def create_inbody_agent():
    """Create and return the Inbody Specialist agent"""
    client = initialize_azure_client()
    if not client:
        return None
    

    Inbody_Specialist = AssistantAgent(
    name="Inbody_Speciallist_agent",
    model_client=client,
    system_message="You are a professional Inbody Speciallist. I will upload an image." \
    "you check if the image is any type of InBody analysis or have any data related to inbody measure"
    "Rule:if not return  'not valid image' "
    "Rule:if yes the image is any type of InBody analysis or have any data related to inbody measure return the measure data as that weight:60 etc "
    "note: make the output text "
    ,
    output_content_type=ImageResponse
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

async def process_inbody_analysis(image) -> dict:
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
        
        # Prepare analysis message
        analysis_message = f"""
        Please check this image
        """
        
        # Create multimodal message with image
        message = MultiModalMessage(content=[image,analysis_message],source="User")
        
        # Get analysis from InBody Specialist
        analysis_output = await inbody_agent.on_messages(
            [message], 
            cancellation_token=CancellationToken()
        )
        
        # Extract the response
        if analysis_output :
            response = analysis_output.chat_message.content
            response = response.model_dump()
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
@router.post('/analyze')
async def analyze_inbody(request: Request):
    """Main endpoint for InBody analysis"""
    try:
        data = await request.json()
        
        # Validate input
        if not data:
            return {"error": "No data provided"}
        
       
        # Extract data
        
        image_url = data.get('inbody_image_url', '')
        image =None
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            image = loop.run_until_complete(
               process_inbody_image(image_url)
            )
        finally:
            loop.close()
        
        # Perform InBody analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                process_inbody_analysis(image)
            )
        finally:
            loop.close()
        
        return result
        
    except Exception as e:
        return {"error": f"Server error: {str(e)}"}

@router.get('/health')
async def inbody_health_check():
    """Health check endpoint for Inbody Specialist"""
    try:
        agent = create_inbody_agent()
        status = "healthy" if agent else "unhealthy"
        return {
            "status": status, 
            "service": "inbody_specialist",
            "agent_available": agent is not None
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "inbody_specialist",
            "error": str(e)
        }

@router.post('/simple_analysis')
async def simple_inbody_analysis(request: Request):
    """Simplified endpoint for basic InBody analysis"""
    try:
        data = await request.json()
        
        if not data or 'query' not in data:
            return {"error": "Query is required"}
        
        query = data['query']
        
        # Initialize Inbody Specialist agent
        inbody_agent = create_inbody_agent()
        
        if not inbody_agent:
            return {"error": "Failed to initialize Inbody Specialist agent"}
        
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
        
        return {"response": result, "status": "success"}
        
    except Exception as e:
        return {"error": f"Server error: {str(e)}"} 
