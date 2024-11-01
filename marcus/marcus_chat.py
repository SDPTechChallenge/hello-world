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
from google.colab import userdata

client = OpenAI(api_key = userdata.get('OPENAI_API_KEY'))

class MarcusChatbot:

  def __init__(self):
    nome_do_modelo='gpt-4o-mini'
    self.nome_do_modelo = nome_do_modelo
    system_message=None
    client=None
    return None

  def call_llm(self, prompt):
    self.prompt = prompt
    completion = client.chat.completions.create(
      model=self.nome_do_modelo,
      messages=[{"role":"user","content":prompt}],
      temperature=0.2,
      top_p=0.7,
      max_tokens=1024,
      stream=False
    )
    response = completion.choices[0].message.content
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

  def document_loading(self):
    filepath = '/MachineLearning-Lecture01.pdf'
    loader = PyPDFLoader(filepath)
    pages = loader.load()
    return pages

  def question_answering(self, question):
     docs = self.document_loading()
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
  
bot = MarcusChatbot()
bot.question_answering("What's the number of the machine learning class?")

chatbot = MarcusChatbot()
chatbot.start_conversation_loop()