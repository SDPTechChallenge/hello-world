from openai import OpenAI
from langchain_community.document_loaders import PyMuPDFLoader as PDFLoader
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
# client = OpenAI(
#     base_url="https://integrate.api.nvidia.com/v1",
#     api_key=os.getenv("NVIDIA_API_KEY")
# )


class DocumentAssistant:

    def __init__(self, system_message=None, model_name='gpt-4o-mini', filepath=""):
        print('Chatbot instanciado com sucesso.')
        self.messages = []  # Armazenar uma lista de mensagem
        self.model_name = model_name  # Modelo de linguagem
        self.system_message = system_message  # Mensagem inicial
        self.document_loaded = False  # Flag booleano se o doc foi carregado ou não
        self.docs = None  # Pode ser preenchido com os docs em test_files
        self.rag_chain = None  # Reutilizar a cadeia RAG em difentes interações
        self.filepath = filepath
        if self.filepath:
            self.load_document(filepath)

    def submit_general_question(self, prompt):
        self.messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model=self.model_name,  # Resgate do modelo
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,  # Respostas mais focadas e previsíveis
            top_p=0.7,  # Soma das probabilidades para manter diversidade nas respostas
            max_tokens=1024,  # Tamanho das respostas
            stream=False
        )
        # Acesso a primeira escolha de resposta do modelo e extração do seu conteúdo
        response = completion.choices[0].message.content

        # Armazenamento dessa resposta no histórico de mensagens do chatbot
        self.messages.append({"role": "assistant", "content": response})

        return response

    # Salva as mensagens armazenadas em um arquivo JSON
    def save_messages_to_file(self, filename="messages_list.json"):
        # Representação string das mensagens
        message_list_string = json.dumps(self.messages)
        # Abre ou cria um arquivo chamado message_list.json, modo de escrita "w"
        open("messages_list.json", "w").write(message_list_string)
        try:
            # Usando 'with' para garantir que o arquivo seja fechado corretamente
            with open(filename, "w") as file:
                file.write(message_list_string)
            print(f"Mensagens salvas com sucesso em '{filename}'.")

        except IOError as e:
            # Captura erros relacionados à entrada/saída
            print(f"Erro ao tentar salvar mensagens em '{filename}': {e}")

        except Exception as e:
            # Captura qualquer outro erro que possa ocorrer
            print(f"Ocorreu um erro inesperado: {e}")

    def load_document(self, filepath):  # Os arquivos estão salvos em filepath
        loader = PDFLoader(filepath)
        print("Loaded document at", filepath)
        self.docs = loader.load()  # Lê conteúdo do PDF e retorna dados
        self.document_loaded = True  # Atualiza se o documento foi carregado com sucesso
        print('[Document loaded]')
        # Prepare the RAG chain
        # Configura uma cadeia RAG usando os dados carregados do documento
        self.prepare_rag_chain()

    def prepare_rag_chain(self):
        # Resgatando o que já foi definido
        llm = ChatOpenAI(model=self.model_name)
        # Divisão do texto em partes menores (chunks), tamanho máximo e sobreposição
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=400)
        # Divisão dos documentos em chunks menores, armazenamento em splits
        splits = text_splitter.split_documents(self.docs)
        print(f'[Splitting finished with {len(splits)} splits]')
        vectorstore = InMemoryVectorStore.from_documents(  # Armazenamento vetorial em memória a partir dos splits
            # Geração de embeddings para recuperação das informações
            documents=splits, embedding=OpenAIEmbeddings()
        )
        # Armazenameto vetorial em objeto recuperador para buscar chunks relevantes
        retriever = vectorstore.as_retriever()

        system_prompt = (  # Orientação do comportamento do Chat
            "You are an assistant for question-answering tasks."
            "Use the following pieces of retrieved context to answer the question."
            "If you don't know the answer, say that you don't know."
            "Use three sentences maximum and keep the answer concise."
            "\n\n"
            "Context:\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages(  # Formatação da interação entre assistente e usuário
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        # Recuperação das informações com geração de respostas baseadas no contexto
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        # Uso do recuperador para exercer RAG
        self.rag_chain = create_retrieval_chain(
            retriever, question_answer_chain)

    def submit_document_question(self, question):  # Pergunta feita pelo usuário
        # Processar a pergunta com base no contexto
        result = self.rag_chain.invoke({"input": question})
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

    def process_user_message(self, message):
        if self.is_question_about_document(message):
            if not self.document_loaded:
                return "No document loaded. Please load a document before asking a document-specific question."
            llm_response = self.submit_document_question(message)['answer']
            return llm_response
        else:
            llm_response = self.submit_general_question(message)
            return llm_response

    @classmethod
    def create(filepath=None):
        return DocumentAssistant(model_name='gpt-4o-mini', filepath=filepath)
