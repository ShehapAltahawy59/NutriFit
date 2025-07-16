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
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def initialize_azure_client():
    """Initialize Azure OpenAI client with proper authentication"""
    try:
        # Azure configuration
        endpoint   = os.environ["AZURE_OPENAI_ENDPOINT"]
        api_key    = os.environ["AZURE_OPENAI_API_KEY"]
        api_ver    = os.environ["AZURE_OPENAI_API_VERSION"]
        deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
        gemini_api_key = os.environ["GEMINI_API_KEY"]
        
        client = AzureOpenAIChatCompletionClient(
            azure_deployment=deployment,
            model=deployment,
            api_version=api_ver,
            azure_endpoint=endpoint,
            api_key=api_key, # For key-based authentication.
        )
        
        gemini_client = OpenAIChatCompletionClient(
        model="gemini-2.5-flash",
        api_key=gemini_api_key,
        model_info=ModelInfo(vision=True, function_calling=True, json_output=True, family="unknown", structured_output=True)
        )

        return client,gemini_client
    except Exception as e:
        print(f"Error initializing Azure client: {e}")
        return None 
