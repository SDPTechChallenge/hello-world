from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import sys
import requests
import base64
import json

load_dotenv()

# os.environ['NVIDIA_API_KEY'] = userdata.get('NVIDIA_API_KEY')

client = OpenAI(
  #base_url = 'https://integrate.api.nvidia.com/v1'
  #api_key = userdata.get('NVIDIA_API_KEY')
)

class MarcusChatbot:

  def __init__(self, system_message=None, model_name='gpt-4o-mini'):
    # Nome do modelo é passado pelo usuário ao instanciar a classe
    print('Chatbot instanciado com sucesso.')
    self.messages = []
    self.model_name = model_name
    self.system_message = system_message
    return None

  def call_llm(self, prompt):
    self.messages.append({"role" : "user", "content" : prompt})
    
    completion = client.chat.completions.create(
      model=self.model_name,
      messages=[{"role":"user","content":prompt}],
      temperature=0.2,
      top_p=0.7,
      max_tokens=1024,
      stream=False
    )
    response = completion.choices[0].message.content
    
    self.messages.append({"role" : "assistant", "content" : response})
    
    return response

  def save_messages_to_file(self, filename="messages_list.json"):
    message_list_string = json.dumps(self.messages)
    open("message_list.json", "w").write(message_list_string)

  def start_conversation_loop(self):
    while True:
      user_message = input("Você: ")
      if user_message.lower() == "quit":
        break

      llm_response = self.call_llm(user_message)
      print(f"Chatbot: {llm_response}")

  def save_messages(self, filename="conversation.json"):
    pass

  def load_document(self, filepath):
    loader = PyPDFLoader(filepath)
    pages = loader.load()
    return pages

  def submit_question(self, question, filepath='test_files/MachineLearning-Lecture01.pdf'):
     docs = self.load_document(filepath)
     llm = ChatOpenAI(model=self.model_name)
     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
     splits = text_splitter.split_documents(docs)
     vectorstore = InMemoryVectorStore.from_documents(
        documents=splits, embedding=OpenAIEmbeddings()
        )
     retriever = vectorstore.as_retriever()
     
     system_prompt = (
        "You are an assistant for question-answering tasks."
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
        )
     
     prompt = ChatPromptTemplate.from_messages(
        [
           ("system", system_prompt),
           ("human", "{input}"),
           ]
           )
     
     question_answer_chain = create_stuff_documents_chain(llm, prompt)
     rag_chain = create_retrieval_chain(retriever, question_answer_chain)
     result = rag_chain.invoke({"input": question})
     return result
  
# bot = MarcusChatbot(model_name="gpt-4o-mini")
# response = bot.submit_question("What's the number of the machine learning class?")
# print(response['answer'])

chatbot = MarcusChatbot()
response = chatbot.submit_question(input('Pergunte sobre o PDF:'))
print(response['answer'])