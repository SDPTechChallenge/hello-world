from openai import OpenAI
from dotenv import load_dotenv
from sqlite3 import DatabaseError, Error
import os
import re
import sqlite3 as sql
import json

load_dotenv()

# Llama 3.2 3B
# Llama 3.1 70B
openai_client = OpenAI()

DB_PATH = 'SQLChatbot.db'

# Classe SQLChatbot


class SQLChatbot:
    def __init__(self, instruction, db_path, few_shot_list=None):
        self.messages = []
        self.llm = OpenAI()
        self.db_path = db_path
        self.messages.append({"role": "system", "content": instruction})
        self.retry_count = 0
        self.debug = True
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
            print('Connected to database at', self.db_path)
            # cursor.execute(create_customer_table_query)  # Cria tabela se não existir
            # cursor.execute(insert_customers_query)  # Insere dados na tabela
            results = cursor.execute(sql_command).fetchall()
            if self.debug:
                print(f'[Obtained results: {str(results)}]')
            connection.commit()
            return results
        except DatabaseError as error:
            self.retry_count += 1
            if self.retry_count > 2:
                self.retry_count = 0  # Resetting the count
                return "Maximum number of tries exceeded. Do not retry."
            else:
                return f'Database error:\n' + str(error) + '\n' + \
                    'Please retry. Check for syntax errors. Do not use quotes around the SQL query.'
        finally:
            connection.close()

    def check_if_tool(self, message: str):
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
            temperature=0.4,
            messages=self.messages
        )

        response_text = response.choices[0].message.content

        sql_command = self.check_if_tool(response_text)

        if (sql_command):
            if self.debug:
                print("[SQL tool call]")
            results = self.execute_sql(sql_command)
            response = self.call_llm(f'Results:\n{str(results)}')
            return response
        else:
            return response_text

    def start_conversation_loop(self):
        # Loop de conversa com o usuário
        while True:
            # Caso o usuário digite "exit", o loop é encerrado e a conversa acaba
            # Se não for digitado "exit" o método "get_completion()" é continuamente chamado
            user_input = input("Você: ")
            if user_input == 'DEBUG':
                self.debug = True
            if user_input.lower() == "exit":
                print("Encerrando a conversa. Até logo!")
                open('conversation_log.json', 'w').write(
                    json.dumps(self.messages))
                break
            response = self.call_llm(user_input)
            print(f"Assistente: {response}")

    def __call__(self, message):
        return self.call_llm(message)

# Carregar instruções para o chatbot
# instruction = open('sql_system_message.txt', 'r').read()


# Open sql_system_message.txt using absolute path
instruction = open(os.path.join(os.path.dirname(__file__),
                   'sql_system_message.txt'), 'r').read()

db_agent = SQLChatbot(instruction, DB_PATH)
# db_agent.start_conversation_loop()


def create_bot():
    # Ensure the db path is absolute
    db_abs_path = os.path.abspath(DB_PATH).replace('server', 'sofia')
    print('Creating bot with db path', db_abs_path)
    sqlbot = SQLChatbot(instruction, db_abs_path)
    return sqlbot

# To list all tables from a sqlite database, use the following query:
# SELECT name FROM sqlite_master WHERE type='table';
