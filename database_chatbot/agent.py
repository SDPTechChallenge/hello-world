from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI()

class Agent:
    def __init__(self, instruction, few_shot_list=None):
        self.messages = []
        self.llm = OpenAI()
        self.messages.append({"role" : "system", "content" : instruction})
        if few_shot_list:
            for index, content in enumerate(few_shot_list):
                role = "user" if index % 2 == 0 else "assistant"
                self.messages.apppend({"role" : role, "content": content})

    def call_llm(self, message):
        self.messages.append({"role" : "user", "content" : message})
        response = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            stream=False,
            messages=self.messages
        )
        response_text = response.choices[0].message.content
        self.messages.append({"role" : "assistant", "content": response_text})
        return response_text

    def start_conversation_loop(self):
        # Implementação do loop de conversa com o usuário.
        while True:
        # Aqui usamos a funcao "input()" para obter a mwndagem do usuário 
        # Caso o mesmo digite "exit", o loop é encerrado e a conversa acaba. 
        # Caso contrário, o método "get_completion()" é continuamente chamado.
            user_input = input("Você: ")
            if user_input.lower() == "exit":
                print("Encerrando a conversa. Até logo!")
                self.save_messages_to_file('chatbot_conversation.json')
                break
            response = self.call_llm(user_input)
            print(f"Assistente: {response}")

    def __call__(self, message):
        return self.call_llm(message)

instruction = open('sql_instructions.txt', 'r').read()

db_agent = Agent(instruction)



