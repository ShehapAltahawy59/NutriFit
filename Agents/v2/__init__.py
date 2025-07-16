from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from pathlib import Path
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient
# Register message types to avoid server-side errors
try:
    from autogen_agentchat.messages import register_message_type, StructuredMessage
    register_message_type(StructuredMessage)
except ImportError:
    pass  # Registration not available in this version

# Load environment variables from the parent directory (root)
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

def initialize_azure_client():
    """Initialize Azure OpenAI client with proper authentication"""
    try:
        # Azure configuration
        
        gemini_api_key = os.environ["GEMINI_API_KEY"]
        
    
        gemini_client = OpenAIChatCompletionClient(
        model="gemini-2.5-flash",
        api_key=gemini_api_key,
        model_info=ModelInfo(vision=True, function_calling=True, json_output=True, family="unknown", structured_output=True)
        )

        return gemini_client
    except Exception as e:
        print(f"Error initializing Azure client: {e}")
        return None 
