from tavily import TavilyClient
from dotenv import load_dotenv
import json 

load_dotenv()

client = TavilyClient()

response = client.search("Stock market")

print(json.dumps(response['results'], indent=2))