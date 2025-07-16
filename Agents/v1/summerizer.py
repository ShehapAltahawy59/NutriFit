import json
from flask import Blueprint, request, jsonify
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_core.models import UserMessage
from autogen_core import Image as AGImage
from PIL import Image
from autogen_agentchat.messages import MultiModalMessage,TextMessage
from io import BytesIO
import requests
import asyncio
from pydantic import BaseModel
from typing import List, Optional
from .. import initialize_azure_client
from flask_cors import cross_origin
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
# Create Blueprint for Gym Trainer
summerizer_bp = Blueprint('summerizer_v1', __name__)

# Pydantic models for fitness training





def create_summerizer_agent():
    """Create and return the summerizer agent"""
    client, = initialize_azure_client()
    if not client:
        return None
    summerizer_system_message = f"""
                            Return the summary of those two plans (workout and diet), 
                            as it will provide that summary as input to an agent that takes in-body analysis and history to generate a new workout and diet plan for the user.
                            Return only the essential details the agent will need as history—no extra text or unnecessary data.
                            Note:the output is text only
                            """
    summerizer = AssistantAgent(
    name="summerizer_agent",
    model_client=client,
    system_message =summerizer_system_message,
    )
    
    return summerizer




async def summerize_workout_plan(plan):
    """Create a comprehensive workout plan"""
    try:
        # Initialize Gym Trainer agent
        summerizer = create_summerizer_agent()
        

        if not summerizer :
            return {"error": "Failed to initialize summerizer agent"}
        
        
        
        # Prepare workout plan message
        
        user_message = f"""
        plans: {plan}
        """
        message = TextMessage(content=user_message, source="user")
        
        Inbody_Speciallist_response = await summerizer.on_messages([message], cancellation_token=CancellationToken())
        summerizer_output = Inbody_Speciallist_response.chat_message.content
        
        # Extract the response
        if summerizer_output:
            response = summerizer_output
            # Convert Pydantic model (or any nested models) to dict
            
        else:
            response = "Unable to summerize plan"
        
        return {
            "summerizer_output": response,
            "recommendations": "summerizeation generated successfully",
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": f"Error creating summerizeation: {str(e)}",
            "status": "error"
        }



# Flask routes for Gym Trainer
