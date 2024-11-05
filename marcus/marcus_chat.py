from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

class MarcusChatbot:

    def __init__(self, system_message=None, model_name='gpt-4o-mini'):
        print('Chatbot instanciado com sucesso.')
        self.messages = [] # Armazenar uma lista de mensagem
        self.model_name = model_name # Modelo de linguagem
        self.system_message = system_message # Mensagem inicial
        self.document_loaded = False  # Flag booleano se o doc foi carregado ou não
        self.docs = None # Pode ser preenchido com os docs em test_files
        self.rag_chain = None  # Reutilizar a cadeia RAG em difentes interações

    def call_llm(self, prompt):
        self.messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model=self.model_name, # Resgate do modelo
            messages=[{"role": "user", "content": prompt}], 
            temperature=0.2, # Respostas mais focadas e previsíveis
            top_p=0.7, # Soma das probabilidades para manter diversidade nas respostas
            max_tokens=1024, # Tamanho das respostas
            stream=False
        )
        response = completion.choices[0].message.content # Acesso a primeira escolha de resposta do modelo e extração do seu conteúdo

        self.messages.append({"role": "assistant", "content": response}) # Armazenamento dessa resposta no histórico de mensagens do chatbot

        return response

    def save_messages_to_file(self, filename="messages_list.json"): # Salva as mensagens armazenadas em um arquivo JSON
        message_list_string = json.dumps(self.messages) # Representação string das mensagens
        open("messages_list.json", "w").write(message_list_string) # Abre ou cria um arquivo chamado message_list.json, modo de escrita "w"
        try: 
            with open(filename, "w") as file: # Usando 'with' para garantir que o arquivo seja fechado corretamente
                file.write(message_list_string)
            print(f"Mensagens salvas com sucesso em '{filename}'.")
        
        except IOError as e:
            print(f"Erro ao tentar salvar mensagens em '{filename}': {e}") # Captura erros relacionados à entrada/saída
        
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}") # Captura qualquer outro erro que possa ocorrer

    def save_messages(self, filename="conversation.json"):
        pass

    def load_document(self, filepath): # Os arquivos estão salvos em filepath
        loader = PyPDFLoader(filepath) 
        self.docs = loader.load() #Lê conteúdo do PDF e retorna dados 
        self.document_loaded = True  # Atualiza se o documento foi carregado com sucesso
        print('[Document loaded]')
        # Prepare the RAG chain
        self.prepare_rag_chain() # Configura uma cadeia RAG usando os dados carregados do documento

    def prepare_rag_chain(self):
        llm = ChatOpenAI(model=self.model_name) # Resgatando o que já foi definido
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400) # Divisão do texto em partes menores (chunks), tamanho máximo e sobreposição
        splits = text_splitter.split_documents(self.docs) # Divisão dos documentos em chunks menores, armazenamento em splits
        print(f'[Splitting finished with {len(splits)} splits]')
        vectorstore = InMemoryVectorStore.from_documents( # Armazenamento vetorial em memória a partir dos splits
            documents=splits, embedding=OpenAIEmbeddings() # Geração de embeddings para recuperação das informações
        )
        retriever = vectorstore.as_retriever() # Armazenameto vetorial em objeto recuperador para buscar chunks relevantes

        system_prompt = ( # Orientação do comportamento do Chat
            "You are an assistant for question-answering tasks."
            "Use the following pieces of retrieved context to answer the question."
            "If you don't know the answer, say that you don't know."
            "Use three sentences maximum and keep the answer concise."
            "\n\n"
            "Context:\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages( # Formatação da interação entre assistente e usuário
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, prompt) # Recuperação das informações com geração de respostas baseadas no contexto
        self.rag_chain = create_retrieval_chain(retriever, question_answer_chain) # Uso do recuperador para exercer RAG

    def submit_question(self, question): # Pergunta feita pelo usuário
        result = self.rag_chain.stream({"input": question}) # Processar a pergunta com base no contexto
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
    
    def start_conversation_loop(self): # Conversa contínua com o usuário
        while True:
            user_message = input("Você: ") # Aguarda a resposta do usuário
            if user_message.lower() == "quit": # Como encerra a conversa
                break

            # Check if the question is about the document
            if self.is_question_about_document(user_message):# Chamando o método já definido para saber se é específico ou genérico
                if not self.document_loaded:
                    # Load the document once
                    self.load_document(filepath='test_files/Attention Is All You Need.pdf')
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
chatbot = MarcusChatbot()

chatbot.save_messages_to_file("messages_list.json") 

# Start the conversation loop
chatbot.start_conversation_loop()

