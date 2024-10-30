from openai import OpenAI
from dotenv import load_dotenv
import os
import sqlite3 as sql
from sqlite3 import DatabaseError, Error

load_dotenv()

openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

DB_PATH = 'SQLChatbot.db'

# Definir queries para criação e inserção na tabela
create_customer_table_query = '''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    birthdate DATE,
    city TEXT,
    country TEXT
);
'''.strip()

insert_customers_query = '''
INSERT INTO customers (last_name, first_name, birthdate, city, country)
VALUES
('Evans', 'Sarah', '1982-03-12', 'London', 'UK'),
('Brown', 'David', '1987-08-21', 'Manchester', 'UK'),
('Miller', 'Emily', '1992-11-30', 'Birmingham', 'UK'),
('Wilson', 'James', '1975-05-10', 'Liverpool', 'UK'),
('Taylor', 'Laura', '1990-06-25', 'Edinburgh', 'UK'),
('Silva', 'Ana', '1983-04-14', 'São Paulo', 'Brazil'),
('Costa', 'Bruno', '1995-07-22', 'Rio de Janeiro', 'Brazil'),
('Oliveira', 'Carla', '1988-09-16', 'Brasília', 'Brazil'),
('Souza', 'Felipe', '1991-10-08', 'Curitiba', 'Brazil'),
('Pereira', 'Mariana', '1993-12-03', 'Belo Horizonte', 'Brazil');
'''.strip()

# Classe SQLChatbot
class SQLChatbot:
    def __init__(self, instruction, db_path, few_shot_list=None):
        self.messages = []
        self.llm = OpenAI()
        self.db_path = db_path
        self.messages.append({"role": "system", "content": instruction})
        if few_shot_list:
            for index, content in enumerate(few_shot_list):
                role = "user" if index % 2 == 0 else "assistant"
                self.messages.append({"role": role, "content": content})

    def execute_sql(self, sql_query):
        #Executa uma consulta SQL no banco de dados SQLite
        try:
            connection = sql.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute(create_customer_table_query)  # Cria tabela se não existir
            cursor.execute(insert_customers_query)  # Insere dados na tabela
            results = cursor.execute(sql_query).fetchall()
            connection.commit()
            return results
        except DatabaseError as error:
            return f'Erro no banco de dados: {repr(error)}'
        finally:
            connection.close()

    def call_llm(self, message):
        self.messages.append({"role": "user", "content": message})
        
        # Verificar se é um comando SQL
        if message.lower().startswith("sql:"):
            sql_query = message[4:].strip()
            sql_result = self.execute_sql(sql_query)
            response_text = f"Resultado da consulta SQL:\n{sql_result}"
        else:
            # Consulta normal ao modelo
            response = self.llm.chat.completions.create(
                model="gpt-4o-mini",
                stream=False,
                messages=self.messages
            )
            response_text = response.choices[0].message.content

        self.messages.append({"role": "assistant", "content": response_text})
        return response_text

    def start_conversation_loop(self):
        # Loop de conversa com o usuário
        while True:
        # Caso o usuário digite "exit", o loop é encerrado e a conversa acaba
        # Se não for digitado "exit" o método "get_completion()" é continuamente chamado
            user_input = input("Você: ")
            if user_input.lower() == "exit":
                print("Encerrando a conversa. Até logo!")
                break
            response = self.call_llm(user_input)
            print(f"Assistente: {response}")

    def __call__(self, message):
        return self.call_llm(message)

# Carregar instruções para o chatbot
instruction = open('sql_system_message.txt', 'r').read()

db_agent = SQLChatbot(instruction, DB_PATH)
db_agent.start_conversation_loop()
