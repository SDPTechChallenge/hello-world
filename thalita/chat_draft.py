from openai import OpenAI
from dotenv import load_dotenv
from tavily import TavilyClient
import json
import os 
import re

load_dotenv()

load_dotenv()

def create_client(vendor='openai') -> OpenAI:
    if vendor == "openai":
        client = OpenAI()
        return client
    else:
        client = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = os.getenv('NVIDIA_API_KEY')
        )
        return client
        

class BasicChatbotWithTool:
  def __init__(self, model_name = "gpt-4o-mini", system_message=None, llm_client=OpenAI(), fewshot_list=[]):
    self.model_name = model_name
    self.messages = []
    self.llm_client = llm_client
    self.tav_client = TavilyClient()

    if system_message is not None:
      self.messages.append({"role" : "system", "content" : system_message})
      
    if fewshot_list:
      for index, content in enumerate(fewshot_list):
        role = "user" if index % 2 == 0 else "assistant"
        self.messages.append({"role": role, "content": content})

  def get_completion(self, message):
    # A mensagem é sempre um dict contendo as chaves "role" e "content".
    # A chave "role" pode ser "system" (mensagem de sistema), "assistant" (resposta da LLM) ou "user" (mensagem do usuário).
    
    # Inicialmente, inserimos a mensagem do usuário (argumento "message") na lista de mensagens.
    self.messages.append({"role" : "user", "content" : message})
    
    # Chamada padrão da API da OpenAI, que foi instanciada no construtor da classe como "llm_client".
    # Importante: a lista completa de mensagens trocadas até o momento é passada para o modelo em todas as chamadas
    # Isso assegura que o contexto, ou memória da conversa, será mantida ao longo da interacao.
    response = self.llm_client.chat.completions.create(
        model=self.model_name, 
        temperature=0.2, 
        messages=self.messages, 
        stream=False
    )

    # Aqui, extraímos o conteúdo da resposta da LLM e o adicionamos à lista de mensagens.
    response_text = response.choices[0].message.content
    self.messages.append({'role': 'assistant', 'content': response_text})
    
    tool_call_string = self.find_tool_call(response_text)
    
    if tool_call_string:
      search_results = self.perform_internet_search(tool_call_string)
      results_string = f'<QUERY_RESULTS>{search_results}</QUERY_RESULTS>'
      llm_response = self.get_completion(results_string)
      return llm_response
    else:
      # Enfim, retornamos a string contendo a resposta da LLM.
      return response_text

  def get_messages(self):
    return self.messages
  
  def find_tool_call(self, text):
    pattern = r'NEWS_TOOL_CALL\s*:\s*(.*)'
    match = re.match(pattern, text, re.MULTILINE)
    if match:
      news_topic = match.groups()[0].strip()
      return news_topic
    else:
      return None
    
  def perform_internet_search(self, query, topic = "news"):
    tav_response = self.tav_client.search(query, topic=topic)
    contents = [res['content'] for res in tav_response['results']]
    separator = "\n----------\n"
    joined_contents = separator.join(contents)
    return joined_contents

  def save_messages_to_file(self, filename):
      with open('chat_messages_2.json', 'w', encoding='utf-8') as file:
        json.dump(self.messages, file, ensure_ascii=False, indent=4)
        
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
  
with open('chat_messages.json', 'r', encoding="utf-8") as file:
  fewshot_list = json.load(file)
  
client = create_client('nvidia')
bot = BasicChatbotWithTool(
  system_message=open('./instructions.txt').read(), 
  llm_client=client, 
  model_name="meta/llama-3.1-70b-instruct",
  )

bot.start_conversation_loop()
