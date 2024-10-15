from openai import OpenAI
import os

class BasicChabot():
    def __init__(self, model_name='model_name_here', system_message = None):
        self.model_name = None
        self.messages = None
        self.llm_client = None
        # Replace 'None' with the necessary code. Remember that 'llm_client' is an instance of the OpenAI object and
        # 'messages' is a list of message objects. This list grows as the chat progresses and new messages are exchanged.
        # Message object example: {'role': 'system | user | assistant', 'content': 'This is a message from the system, assistant or user'} 
        
    def get_completion(self, message):
        # Append user message to 'self.messages'
        # Call LLM with user message and wait for response
        # Append response text to 'self.messages' with the 'assistant' role
        # Return response text
        pass
    
    def get_messages(self):
        # Return the list of all exchanged messages. One line of code.
        pass 
    
    # Other important or necessary class methods
    
cool_chatbot = BasicChabot("model_name", "You are a helpful assistant who specializes in...")
cool_chatbot.get_completions("Hello! Write a short poem about life.")
