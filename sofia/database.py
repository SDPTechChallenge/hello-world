import sqlite3 as sql


def run_pipeline(db_path='SQLChatbot.db', schema_file='sql_system_message.txt'):
    print(f'Running pipeline with db_path: {db_path} and schema_file: {schema_file}')
    exit(0)

    # Conecta ao banco de dados SQLite e salva a estrutura do banco no arquivo de esquema.
    try:
        connection = sql.connect(db_path)
        cursor = connection.cursor()
        print(f'Conectado ao banco de dados em: {db_path}')

        # Obtém as tabelas do banco de dados
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Monta a descrição do esquema
        schema_description = []
        for table in tables:
            table_name = table[0]
            schema_description.append(f"Table: {table_name}")
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            for column in columns:
                schema_description.append(f" - {column[1]} ({column[2]})")

        # Converte o esquema em uma única string
        table_schema_str = "\n".join(schema_description)

        # Lê o conteúdo do arquivo modelo e substitui o placeholder pelo esquema gerado
        with open(schema_file, 'r') as f:
            content = f.read()

        content = content.replace("{table_schema}", table_schema_str)

        # Escreve o conteúdo atualizado no arquivo de esquema
        with open(schema_file, 'w') as f:
            f.write(content)
        print(f'Esquema salvo e atualizado em: {schema_file}')

    except sql.DatabaseError as e:
        print(f"Erro ao conectar ao banco de dados ou obter esquema: {e}")

    finally:
        connection.close()
