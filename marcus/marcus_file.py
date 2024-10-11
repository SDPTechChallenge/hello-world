# sempre começar com git pull
# já criei o .env e lá estão as minhas chaves. No terminal fiz a instalação: pip install python-dotenv
# depois instalei open ai com install openai
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])