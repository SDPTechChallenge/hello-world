from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import sqlite3 as sql
import json
from .database import run_pipeline  # Importa o pipeline do database.py

load_dotenv()

client = OpenAI()

DB_PATH = 'SQLChatbot.db'
SCHEMA_FILE = 'sql_system_message.txt'

# Executa o pipeline de dados antes de inicializar o chatbot
# run_pipeline(os.path.abspath(os.path.join(os.path.dirname(__file__), DB_PATH)),
#  os.path.abspath(os.path.join(os.path.dirname(__file__), SCHEMA_FILE)))


class SQLAssistant:
    def __init__(self, instruction, db_path, few_shot_list=None, table_schema=""):
        self.messages = []
        self.llm = OpenAI()
        self.db_path = db_path
        self.messages.append({"role": "system", "content": instruction})
        self.retry_count = 0
        self.debug = False  # Desativa o modo debug por padrão
        self.__call__ = self.call_llm
        print("Chatbot inicializado com sucesso.")
        if few_shot_list:
            for index, content in enumerate(few_shot_list):
                role = "user" if index % 2 == 0 else "assistant"
                self.messages.append({"role": role, "content": content})

    def execute_sql(self, sql_command):
        # Executa uma consulta SQL no banco de dados SQLite
        try:
            if self.debug:
                print(f'[Executing query: {sql_command}]')
            connection = sql.connect(self.db_path)
            cursor = connection.cursor()
            results = cursor.execute(sql_command).fetchall()
            if self.debug:
                print(f'[Obtained results: {str(results)}]')
            connection.commit()
            return results
        except sql.DatabaseError as error:
            self.retry_count += 1
            if self.retry_count > 2:
                self.retry_count = 0  # Resetando o contador
                return "Maximum number of tries exceeded. Do not retry."
            else:
                return f'Database error:\n' + str(error) + '\n' + \
                    'Please retry. Check for syntax errors. Do not use quotes around the SQL query.'
        finally:
            connection.close()

    def check_if_tool(self, message: str):
        # Verifica se a resposta contém um comando SQL
        pattern = r'SQL_TOOL_CALL\s*:\s*(.*)'
        match = re.match(pattern, message, re.MULTILINE)
        if match:
            sql_command = match.groups()[0]
            return sql_command
        else:
            return None

    def call_llm(self, message, stream=False, callback=None):
        self.messages.append({"role": "user", "content": message})

        # Consulta ao modelo
        response = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            stream=stream,
            temperature=0.2,
            messages=self.messages
        )

        response_text = response.choices[0].message.content

        sql_command = self.check_if_tool(response_text)

        if sql_command:
            results = self.execute_sql(sql_command)
            response = self.call_llm(f'Results:\n{str(results)}')
            return response
        else:
            return response_text

    def start_conversation_loop(self):
        # Loop de conversa com o usuário
        while True:
            user_input = input("Você: ")
            if user_input.upper() == 'DEBUG':
                self.debug = True  # Ativa o modo debug
                print("Modo DEBUG ativado.")
                continue  # Pede uma nova entrada do usuário
            if user_input.lower() == "exit":
                print("Encerrando a conversa. Até logo!")
                open('conversation_log.json', 'w').write(
                    json.dumps(self.messages))
                break
            response = self.call_llm(user_input)
            print(f"Assistente: {response}")

    def __call__(self, message):
        return self.call_llm(message)

    @classmethod
    def create(cls):
        instructions_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), SCHEMA_FILE))
        with open(instructions_file, 'r') as f:
            instruction = f.read()
        db_abs_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), DB_PATH))
        print('Creating bot with db path', db_abs_path)
        sqlbot = cls(instruction, db_abs_path)
        return sqlbot


# Carregar instruções para o chatbot
# with open(SCHEMA_FILE, 'r') as f:
#     instruction = f.read()


# def create_bot():
#     db_abs_path = os.path.abspath(DB_PATH).replace('server', 'sofia')
#     print('Creating bot with db path', db_abs_path)
#     sqlbot = SQLChatbot(instruction, db_abs_path)
#     return sqlbot
