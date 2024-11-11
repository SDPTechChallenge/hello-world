from general_assistant import GeneralAssistant
import json

with open('internet_search/instructions.txt', 'r', encoding='utf-8') as file:
    instructions = file.read()

with open('conversation_logs/news_few_shot.json', 'r', encoding='utf-8') as file:
    fewshot_list = json.load(file)

LLAMA_MODEL = 'meta/llama-3.2-3b-instruct'
MISTRAL_MODEL = 'mistralai/mistral-7b-instruct-v0.3'
GPT_MODEL = 'gpt-4o-mini'

assistant = GeneralAssistant(
    GPT_MODEL, instructions=instructions, fewshow_list=fewshot_list)


def conversation_loop():
    while True:
        user_input = input("You: ")
        if user_input == 'exit':
            break
        response = assistant(user_input, stream=False, max_tokens=1024)
        print("Assistant: ", end='', flush=True)
        print(response)
        # for chunk in response:
        #     if chunk is not None:
        #         print(chunk, end='', flush=True)
        print()


conversation_loop()

# print(assistant.messages[-1]['content'])
