import sqlite3 as sql

# File names
customers_file = 'customers.csv'

database = 'SQLChatbot.db'

# Implement function that reads table columns and adds the table schema to the system message 

def load_to_sqlite(df, table_name, conn):
    df.to_sql(table_name, conn, if_exists='replace', index=False, chunksize=500)
    print(f"{table_name} table created successfully.")

def run_pipeline():
    # Connect to the database
    conn = sqlite3.connect(database)
    
    try:
        # Load CSV files
        customers_df = pd.read_csv(customers_file)
        
        # Load data into SQLite tables
        load_to_sqlite(customers_df, 'customers', conn)
        
        print("Data pipeline completed successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

# Run the pipeline
run_pipeline()
