import sqlite3 as sql
from sqlite3 import Error
from argparse import ArgumentParser

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


parser = ArgumentParser()
parser.add_argument('--sql')
args = parser.parse_args()

connection = sql.connect('test.db')
cursor = connection.cursor()

if args.sql:
    results = connection.cursor().execute(args.sql).fetchall()
    print(results)

def insert_customers_into_table():
    try:
        count = cursor.execute(insert_customers_query).rowcount
        connection.commit()
        print(f'Successfully inserted {count} customers')
    except sql.DatabaseError as error:
        print('There was an error.\n' + repr(error))
    except:
        print("There was an error.")

def create_table():
    try:
        cursor.execute(create_customer_table_query)
        connection.commit()
        print("Table created successfully.")
    except sql.DatabaseError as error:
        print('There was an error.\n' + repr(error))
    except:
        print("There was an error.")

# create_table()
# insert_customers_into_table()
connection.close()
    
    
    
