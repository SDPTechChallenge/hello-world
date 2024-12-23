from openai import OpenAI
from langchain_community.document_loaders import PyMuPDFLoader as PDFLoader
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

client = OpenAI()


class MarcusChatbot:

    def __init__(self, system_message=None, model_name='gpt-4o-mini'):
        print('Chatbot instanciado com sucesso.')
        self.messages = []
        self.model_name = model_name
        self.system_message = system_message
        self.document_loaded = False  # Flag to check if document is loaded
        self.docs = None
        self.rag_chain = None  # Store the RAG chain for reuse

    def call_llm(self, prompt):
        self.messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )
        response = completion.choices[0].message.content

        self.messages.append({"role": "assistant", "content": response})

        return response

    def save_messages_to_file(self, filename="messages_list.json"):
        message_list_string = json.dumps(self.messages)
        open("message_list.json", "w").write(message_list_string)

    def save_messages(self, filename="conversation.json"):
        pass

    def load_document(self, filepath):
        loader = PDFLoader(filepath)
        self.docs = loader.load()
        self.document_loaded = True  # Update the flag
        print('[Document loaded]')
        # Prepare the RAG chain
        self.prepare_rag_chain()

    def prepare_rag_chain(self):
        llm = ChatOpenAI(model=self.model_name)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=400)
        splits = text_splitter.split_documents(self.docs)
        print(f'[Splitting finished with {len(splits)} splits]')
        vectorstore = InMemoryVectorStore.from_documents(
            documents=splits, embedding=OpenAIEmbeddings()
        )
        retriever = vectorstore.as_retriever()

        system_prompt = (
            "You are an assistant for question-answering tasks."
            "Use the following pieces of retrieved context to answer the question."
            "If you don't know the answer, say that you don't know."
            "Use three sentences maximum and keep the answer concise."
            "Answer in Portuguese if the user speaks in that language. Translate as necessary."
            "\n\n"
            "Context:\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        self.rag_chain = create_retrieval_chain(
            retriever, question_answer_chain)

    def submit_question(self, question):
        result = self.rag_chain.stream({"input": question})
        return result

    def is_question_about_document(self, question):
        prompt = f"""
        Determine whether the following is a general question that can be answered without context or a specific question that is likely based on a source or document the user has read or seen and is inquiring about.
        If it is likely a generic question, simply say "Generic". If it is likely context-specific, simply say "Specific".

        Question: "{question}"
        """
        completion = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=3,
            stream=False
        )
        response = completion.choices[0].message.content.strip().upper()
        return ('SPECIFIC' in response)

    def start_conversation_loop(self):
        while True:
            user_message = input("Você: ")
            if user_message.lower() == "quit":
                break

            # Check if the question is about the document
            if self.is_question_about_document(user_message):
                if not self.document_loaded:
                    # Load the document once
                    self.load_document(
                        filepath='test_files/Attention Is All You Need.pdf')
                llm_response = self.submit_question(user_message)
                print('[SPECIFIC] ', end="", flush=True)
                for chunk in llm_response:
                    if chunk and 'answer' in chunk:
                        print(chunk['answer'], end="", flush=True)
                print()
            else:
                llm_response = self.call_llm(user_message)
                print(f"Chatbot: [GENERIC] {llm_response}")

# Instantiate the chatbot
# chatbot = MarcusChatbot()

# Start the conversation loop
# chatbot.start_conversation_loop()
