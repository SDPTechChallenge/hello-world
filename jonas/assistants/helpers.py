from tavily import TavilyClient
from dotenv import load_dotenv
import json

load_dotenv()

tav_client = TavilyClient()

response_basic = tav_client.search(
    "NVIDIA", search_depth='basic', topic='general')
response_advanced = tav_client.search(
    "NVIDIA", search_depth="advanced", topic="general")

# Save both to file:

with open('basic_search_results.json', 'w', encoding='utf-8') as file:
    json.dump(response_basic, file, ensure_ascii=False, indent=4)

with open('advanced_search_results.json', 'w', encoding='utf-8') as file:
    json.dump(response_advanced, file, ensure_ascii=False, indent=4)
