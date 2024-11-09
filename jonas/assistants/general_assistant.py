from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()


class GeneralAssistant():
    def __init__(self, client=OpenAI(), model_id="gpt-4o-mini", instructions="", fewshow_list=[]):
        self.client = OpenAI()
        self.messages = []
        self.client = client
        self.model_id = model_id
        self.conversation_id = datetime.now().strftime("%Y%m%d%H%M%S")
        if instructions:
            self.messages.append({'role': 'system', 'content': instructions})
        if fewshow_list:
            self.messages.extend(fewshow_list)
            
    def _stream_generator(self, stream : Stream[ChatCompletionChunk]):
        complete_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content is not None:
                complete_response += content
                yield content
        self.messages.append({'role': 'assistant', 'content': complete_response})

    def _save_messages_to_file(self):
        with open(f"conversation_logs/{self.conversation_id}.txt", "w") as f:
            for message in self.messages:
                f.write(f"{message['role']}: {message['content']}\n")
    
    def call_llm(self, prompt, stream=False,  **kwargs):
        self.messages.append({'role': 'user', 'content': prompt})

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            stream=stream,
            messages=self.messages,
            **kwargs
        )

        if stream:
            return self._stream_generator(completion)
        else:
            return completion.choices[0].message.content
        
assistant = GeneralAssistant()