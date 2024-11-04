import sqlite3 as sql
import pandas as pd

# File names
customers_files = [{"filepath" : "Mall_Customers.csv", "table" : "mall_customers"}]

database = 'SQLChatbot.db'

# Implement function that reads table columns and adds the table schema to the system message 

def load_to_sqlite(df : pd.DataFrame, table_name : str, conn : sql.Connection):
    df.to_sql(table_name, conn, if_exists='replace', index=False, chunksize=500)
    print(f"{table_name} table created successfully.")

def run_pipeline():
    # Connect to the database
    conn = sql.connect(database)
    
    try:
        for file in customers_files:
            # Load CSV files
            df = pd.read_csv(f'data/{file['filepath']}')        
            # Load data into SQLite tables
            load_to_sqlite(df, file['table'], conn)
        
        print("Data pipeline completed successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

# Run the pipeline
run_pipeline()
