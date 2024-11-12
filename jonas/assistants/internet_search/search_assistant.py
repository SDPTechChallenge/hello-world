from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class Assistant:
    def __init__(self, model_id: str = 'gpt-4o-mini', instructions: str = "", fewshot_list: list[str] = []):
        self.client = self._create_client('gpt-4o-mini')
        self.model_id = model_id
        self.messages = []
        if instructions:
            self.messages.append({"role": "system", "content": instructions})
        if fewshot_list:
            self.messages.extend(fewshot_list)

    def __call__(self, message: str):
        return self.get_completion(message)

    def get_completion(self, message: str):

        self.messages.append({"role": "user", "content": message})

        completions = self.client.chat.completions.create(
            model=self.model_id,
            temperature=0.4,
            messages=self.messages,
            stream=False
        )

        response = completions.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': response})
        return response

    def _create_client(cls, model_id: str):
        client = OpenAI()
        if model_id.startswith('gpt'):
            return client
        elif model_id.startswith('meta') or model_id.startswith('mistral'):
            print(f'Using model ID: {model_id}')
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=os.getenv('NVIDIA_API_KEY')
            )
            return client
        else:
            print('Invalid model ID. Defaulting to OpenAI API.')
            return client


prompt = """You are an intent classifier. Your task is to classify the intent of the prompt below into one of the following categories:

- Support
- Sales
- Billing
- Other

Your response must be as concise as possible. Output the intent (single word) and nothing more.

User message: {user_message}
"""

intent_classifier = Assistant()
result = intent_classifier(prompt.format(
    user_message=input('You:')))
print(result)
