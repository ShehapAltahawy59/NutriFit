from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from pathlib import Path

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

        client = AzureOpenAIChatCompletionClient(
            azure_deployment=deployment,
            model=deployment,
            api_version=api_ver,
            azure_endpoint=endpoint,
            api_key=api_key, # For key-based authentication.
        )

        return client
    except Exception as e:
        print(f"Error initializing Azure client: {e}")
        return None 
