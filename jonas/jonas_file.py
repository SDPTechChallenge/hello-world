from dotenv import load_dotenv
from openai import OpenAI
from openai import OpenAI
import os 

load_dotenv()


client = OpenAI(
  api_key=os.getenv('NVIDIA_API_KEY'),
  base_url = "https://integrate.api.nvidia.com/v1",
)

completion = client.chat.completions.create(
  model="meta/llama-3.1-405b-instruct",
  messages=[{"role":"user","content":"What are the capitals of France and Russia?"}],
  temperature=0.2,
  top_p=0.7,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")