from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_client = OpenAI()

prompt = str(input("Como posso te ajudar hoje? "))

response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)

response_content = response.choices[0].message.content
print(response_content)


'''
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv("NVIDIA_API_KEY")
)

def call_llm(prompt):
    completion = client.chat.completions.create(
        model="meta/llama-3.1-405b-instruct",
        messages=[{"role":"user","content": prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

call_llm("Qual a capital da França e Luxemburgo? Responda em JSON.")
'''


