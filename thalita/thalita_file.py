# no diretorio hello world, sempre começar com git pull, em seguida git add . e depois git commit -m "a mensagem aqui" e ao final git push

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

