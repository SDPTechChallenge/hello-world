from openai import OpenAI
from dotenv import load_dotenv
from typing import Literal
import os

load_dotenv()

Vendor = Literal['openai', 'nvidia']

def create_client(vendor : Vendor = 'openai') -> OpenAI:
    if vendor == "openai":
        client = OpenAI()
        return client
    else:
        client = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = os.getenv('NVIDIA_API_KEY')
        )
        
__all__= [create_client]