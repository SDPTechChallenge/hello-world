from general_assistant import GeneralAssistant

with open('internet_search/instructions.txt', 'r', encoding='utf-8') as file:
    instructions = file.read()

assistant = GeneralAssistant(
    'meta/llama-3.2-3b-instruct', instructions=instructions)


def conversation_loop():
    while True:
        user_input = input("You: ")
        if user_input == 'exit':
            break
        response = assistant.call_llm(user_input, stream=True, max_tokens=1024)
        print("Assistant: ", end='', flush=True)
        for chunk in response:

            if chunk is not None:
                print(chunk, end='', flush=True)
        print()


conversation_loop()

# print(assistant.messages[-1]['content'])
