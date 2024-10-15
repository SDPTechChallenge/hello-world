from openai import OpenAI
import os

# Remove the 'pass' statements. These are placeholders for actual code.

class BasicChatbot():
    def __init__(self, model_name='model_name_here', system_message = None):
        self.model_name = None
        self.messages = None
        self.llm_client = None
        # Replace 'None' with the necessary code. Remember that 'llm_client' is an instance of the OpenAI object and
        # 'messages' is a list of message objects. This list grows as the chat progresses and new messages are exchanged.
        # Message object example: {'role': 'system | user | assistant', 'content': 'This is a message from the system, assistant or user'} 
        # The 'example_conversation.json' file contains an example of a list of messages
        
    def get_completion(self, message):
        pass
        # 1) Append user message to 'self.messages'
        # 2) Call LLM with user message and wait for response
        # 3) Append response text to 'self.messages' with the 'assistant' role
        # 4) Return response text
    
    def get_messages(self):
        pass
        # Return the list of all exchanged messages
             
    def save_messages_to_file(self, filename):
        pass
        # This method should take the list of messages and save it as a JSON file in the current folder
        # Tip: for saving files, use the 'open' method
    
    # Other important or necessary class methods
    
# The code below should work after the correct implementation
cool_chatbot = BasicChabot("model_name", "You are a helpful assistant who specializes in...")
cool_chatbot.get_completions("Hello! Write a short poem about life.")


