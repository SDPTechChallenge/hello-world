from openai import OpenAI
from dotenv import load_dotenv
import json
import os 
import re

load_dotenv()

# A string abaixo é uma mensagem de sistema que fornece instruções à LLM sobre como responder e agir.
# Mensagens de sistema são a primeira mensagem incluída na lista de mensagens enviadas em cada chamada.
# Elas orientam o comportamento da LLM, fornecendo instrucoes, diretrizes e exemplos sobre como ela deve responder.

primer = "You are a friendly, helpful assistant. Answer the user's questions in a concise manner."

class BasicChatbot:
  def __init__(self, model_name = "gpt-4o-mini", system_message=None):
    self.model_name = model_name
    self.messages = []
    self.llm_client = OpenAI()
    
    if system_message is None:
      self.messages.append({"role" : "system", "content" : primer})
    else:
      self.messages.append({"role" : "system", "content" : system_message})

  def get_completion(self, message):
    # A mensagem é sempre um dict contendo as chaves "role" e "content".
    # A chave "role" pode ser "system" (mensagem de sistema), "assistant" (resposta da LLM) ou "user" (mensagem do usuário).

    self.messages.append({"role" : "user", "content" : message})
    
    # Chamada padrão da API da OpenAI, que foi instanciada no construtor da classe como "llm_client".
    response = self.llm_client.chat.completions.create(
        model=self.model_name, 
        temperature=0.2, 
        messages=self.messages, 
        stream=False
    )

    # Aqui, extraímos o conteúdo da resposta da LLM e o adicionamos à lista de mensagens.
    response_text = response.choices[0].message.content
    self.messages.append({'role': 'assistant', 'content': response_text})
      
    # Retornamos a string contendo o texto da resposta da LLM.
    return response_text

  def get_messages(self):
    # Um método simples que apenas retorna a lista de mensagens trocadas com o modelo até o momento.
    return self.messages

  def save_messages_to_file(self, filename):
    # Método que salva a lista de mensagens em um arquivo com o nome do argumento "filename"
    with open(filename, 'w') as file:
        json.dump(self.messages, file)
        
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
      response = self.get_completion(user_input)
      print(f"Assistente: {response}")
  
  # __call__ é um método especial ("magic method" ou "dunder method") que permite chamar o objeto instanciado como se ele fosse uma função.
  # Neste caso, ele serve apenas como um atalho para o método interno "get_completion()".
  def __call__(self, message):
    return self.get_completion(message)