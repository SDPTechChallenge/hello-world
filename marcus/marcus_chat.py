from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import os
import sys
import requests, base64
import getpass
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

class MarcusChatbot:

  def __init__(self, system_message=None, nome_do_modelo='gpt-4o-mini'):
    # Nome do modelo é passado pelo usuário ao instanciar a classe
    print('Chatbot instanciado com sucesso.')
    self.messages = []
    self.nome_do_modelo = nome_do_modelo
    self.system_message = system_message
    return None

  def call_llm(self, prompt):
    self.messages.append({"role" : "user", "content" : prompt})
    
    completion = client.chat.completions.create(
      model=self.nome_do_modelo,
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

  def document_loading(self, filepath):
    loader = PyPDFLoader(filepath)
    pages = loader.load()
    return pages

  def question_answering(self, question, filepath='test_files/MachineLearning-Lecture01.pdf'):
     docs = self.document_loading(filepath)
     llm = ChatOpenAI(model=self.nome_do_modelo)
     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
     splits = text_splitter.split_documents(docs)
     vectorstore = InMemoryVectorStore.from_documents(
        documents=splits, embedding=OpenAIEmbeddings()
        )
     retriever = vectorstore.as_retriever()
     system_prompt = (
        "You are an assistant for question-answering tasks. "
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
     results = rag_chain.invoke({"input": question})
     return results
  
bot = MarcusChatbot(nome_do_modelo="gpt-4o-mini")
bot.question_answering("What's the number of the machine learning class?")

chatbot = MarcusChatbot()
chatbot.question_answering(input('Pergunte sobre o PDF:'))