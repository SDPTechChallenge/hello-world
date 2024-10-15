# sempre começar com git pull

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

response_content = response.choices[0].message.content

print(response_content)

