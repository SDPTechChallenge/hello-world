import sqlite3 as sql

connection = sql.connect('SQLChatbot.db')
cursor = connection.cursor()

results = cursor.execute("SELECT SUM(strftime('%Y', 'now') - strftime('%Y', birthdate)) FROM customers WHERE country = 'UK'").fetchall()
print(str(results))

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

