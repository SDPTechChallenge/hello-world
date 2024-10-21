from openai import OpenAI
from dotenv import load_dotenv
import json
import os 
import re

load_dotenv()

# A string abaixo é uma mensagem de sistema que fornece instruções à LLM sobre como agir.
# Mensagens de sistema são a primeira mensagem incluída na lista de mensagens enviadas em cada chamada.
# Elas orientam o comportamento da LLM, fornecendo diretrizes sobre como ela deve responder.
# No caso deste chatbot, estamos configurando a LLM para chamar uma "ferramenta" quando necessário.
# A lógica externa (neste caso, uma ferramenta de cálculo) é acionada com a chamada 'calculate'.
# Abaixo, há exemplos de conversas, que ajudam a definir o comportamento desejado do modelo, chamado de "few-shot prompting".

primer = """
You are a friendly, helpful assistant. Your task is to provide concise and helpful answers to general user questions.
The user may ask you to perform a mathematical calculation, in which case you MUST call a tool named "calculate".
Upon calling the tool, the user will provide you with the calculation's answer within <ANSWER> tags. You will then provide the answer as a response back to the user.
The tool call must be formatted as follows:

calculate : <calculation_to_be_performed>

Conversation example:
User: Hello there!
Assistant: Hello! How can I help you today?
User: What is the capital of France?
Assistant: The capital of France is Paris.
User: Cool. How much is 11 x 8.5?
Assistant: calculate : 11 * 8.5
User: <ANSWER>93.5</ANSWER>
Assistant: The answer is 93.50. Is there anything else I can help you with?
User: Yes. Who was the first president of the United States?
Assistant: The first president of the United States was George Washington, who served from 1789 to 1797.
User: Cool. How much is 1797 divided by 9 plus 4.1239 squared?
Assistant: calculate: 1797 / 9 + 4.1239 ** 2
User: <ANSWER>216.67321787666666</ANSWER>
Assistant: The answer is 216.67.
User: Thanks!

You should format the argument of 'calculate' as an input to the "eval" function in Python.
"""

class BasicChatbot:
  def __init__(self, model_name = "gpt-4o-mini", system_message=None):
    self.model_name = model_name
    self.messages = []
    self.llm_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Se nenhuma mensagem de sistema for passada para o construtor da classe,
    # usamos o "primer" (instruções acima). Caso contrário, usamos a mensagem
    # de sistema que foi passada para o construtor. Por padrão, ela é 'None',
    # ou seja, usa-se o primer.
    if system_message is None:
      self.messages.append({"role" : "system", "content" : primer})
    else:
      self.messages.append({"role" : "system", "content" : system_message})

  def get_completion(self, message=None):
    # A mensagem é sempre um dict contendo as chaves "role" e "content".
    # A chave "role" pode ser "system" (mensagem de sistema), "assistant" (resposta da LLM) ou "user" (mensagem do usuário).
    
    # Aqui, se o método tiver sido chamado com uma mensagem do usuário, inserimos a mesma na lista.
    # Fazemos esta verificação porque haverá casos, neste Chatbot em particular, em que este método será 
    # chamado sem uma nova mensagem do usuário.
    if message: 
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
    
    # Abaixo, verificamos se a resposta da LLM contém o padrão "calculate : <algum_calculo>".
    calc_result = self.get_calculation(response_text)
    
    # Caso o padrão seja encontrado, "calc_result" conterá o resultado do cálculo, que será enviado à LLM.
    if calc_result:
      self.messages.append({'role': 'user', 'content' : f'<ANSWER>{calc_result}</ANSWER>'})
      # Após inserir o resultado do cálculo na lista de mensagens, chamamos a LLM novamente.
      # Com a resposta no formato <ANSWER>Resultado</ANSWER>, a LLM reconhecerá o uso da ferramenta.
      response_text = self.get_completion()
      
    # Retornamos a string contendo o texto da resposta da LLM.
    return response_text

  def get_messages(self):
    return self.messages

  def get_calculation(self, text):
    pattern = re.match(r'calculate\s?\:\s?(.*)', text)
    # Esta é uma expressão regular (RegEx). Usamos isto para encontrar texto que siga um determinado padrão em uma string.
    # Neste caso, estamos procurando o padrão "calculate : <algum_calculo>" dentro da string.
    
    if pattern:
      # Se o padrão for encontrado, 1) extraímos o cálculo da string e 2) o executamos
      # usando a função "eval", que avalia expressões fornecidas como string.
      return eval(pattern.groups()[0].strip())
    else:
      # Caso o padrão não seja encontrado, ou seja, a mensagem não contém um pedido de cálculo,
      # retornamos 'None'.
      return None

  def save_messages_to_file(self, filename):
      with open('chat_messages.json', 'w') as file:
        json.dump(self.messages, file)
        
  def start_conversation_loop(self):
    # Implementação do loop de conversa com o usuário.
    while True:
      user_input = input("Você: ")
      if user_input.lower() == "exit":
        print("Encerrando a conversa. Até logo!")
        break
      response = self.get_completion(user_input)
      print(f"Assistente: {response}")
  
  # __call__ é um método especial ("magic method" ou "dunder method") que permite chamar o objeto instanciado como se ele fosse uma função.
  # Neste caso, ele serve apenas como um atalho para o método interno "get_completion()".
  def __call__(self, message):
    return self.get_completion(message)