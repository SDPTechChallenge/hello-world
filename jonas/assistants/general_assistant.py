from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk
from dotenv import load_dotenv
from datetime import datetime
from tavily import TavilyClient
from typing import List, Dict, Annotated
import json
import re
import os

load_dotenv()


def tav_search(query, search_depth='basic', topic='general') -> List[Dict[str, str]]:
    client = TavilyClient()
    response = client.search(
        query, search_depth=search_depth, topic=topic, max_results=4)
    parsed_results = [{'content': res['content'], 'url': res['url']}
                      for res in response['results']]
    return parsed_results


class GeneralAssistant():
    def __init__(self, model_id="gpt-4o-mini", instructions="", fewshow_list=[]):
        self.client = OpenAI()
        self.messages = []
        self.model_id = model_id
        self.client = self._create_client(self.model_id)
        self.conversation_id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.will_call_tool = False
        if instructions:
            self.messages.append({'role': 'system', 'content': instructions})
        if fewshow_list:
            self.messages.extend(fewshow_list)

    def _create_client(self, model_id: str):
        client = OpenAI()
        if model_id.startswith('gpt'):
            return client
        elif model_id.startswith('meta') or model_id.startswith('mistral'):
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=os.getenv('NVIDIA_API_KEY')
            )
            return client
        else:
            print('Invalid model ID. Defaulting to OpenAI API.')
            return client

    def _stream_generator(self, stream: Stream[ChatCompletionChunk], callback: function = None):
        complete_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content is not None:
                complete_response += content
                if 'NEWS_TOOL_CALL' in content.upper():
                    self.will_call_tool = True
                yield content
        if self.will_call_tool:
            tool_args = callback(complete_response)
            self.tav_search_results = tav_search(tool_args)

        self.messages.append(
            {'role': 'assistant', 'content': complete_response})

        self._save_messages_to_file()

    def _save_messages_to_file(self):
        with open(f"conversation_logs/{self.conversation_id}.json", "w") as file:
            json.dump(self.messages, file)

    def call_llm(self, prompt, callback: function, stream=False,  **kwargs):
        self.messages.append({'role': 'user', 'content': prompt})

        completion = self.client.chat.completions.create(
            model=self.model_id,
            stream=stream,
            messages=self.messages,
            **kwargs
        )

        if stream:
            return self._stream_generator(completion, self.find_pattern)
        else:
            response_text = completion.choices[0].message.content
            self.messages.append(
                {'role': 'assistant', 'content': response_text})
            self._save_messages_to_file()
            return response_text

    def find_pattern(self, text: str, pattern=None):
        """
        The the first occurrence of a capture group in a multiline text. 
        In the example below, "news on covid" is the capture group:

        Let's look for news on covid in the latest news headlines.
        NEWS_TOOL_CALL: 'news on covid'
        I have called the tool
        """

        if not pattern:
            pattern = r"NEWS_TOOL_CALL\s*:\s*(.+)\s*"

        match = re.search(pattern, text.strip(), re.MULTILINE)
        if match:
            return match.groups()[0].strip().replace("'", "")
        else:
            return None

    def sumit_message(self, message: str):
        self.call_llm(message, stream=True)
