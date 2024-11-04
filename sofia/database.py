import sqlite3 as sql
import pandas as pd

# File names
customers_file = 'data/Mall_Customers.csv'

database = 'SQLChatbot.db'

# Implement function that reads table columns and adds the table schema to the system message 

def load_to_sqlite(df : pd.DataFrame, table_name : str, conn : sql.Connection):
    df.to_sql(table_name, conn, if_exists='replace', index=False, chunksize=500)
    print(f"{table_name} table created successfully.")

def run_pipeline():
    # Connect to the database
    conn = sql.connect(database)
    
    try:
        # Load CSV files
        customers_df = pd.read_csv(customers_file)
        
        # Load data into SQLite tables
        load_to_sqlite(customers_df, 'mall_customers', conn)
        
        print("Data pipeline completed successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

# Run the pipeline
run_pipeline()
