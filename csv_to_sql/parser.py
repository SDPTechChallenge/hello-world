import pandas as pd
import sqlite3

# Step 1: Define file paths
customers_file = 'customers.csv'
orders_file = 'orders.csv'
database = 'data_pipeline.db'

# Step 2: Define function to load DataFrame into SQLite
def load_to_sqlite(df, table_name, conn):
    df.to_sql(table_name, conn, if_exists='replace', index=False, chunksize=500)
    print(f"{table_name} table created successfully.")

# Step 3: Main function to execute the pipeline
def run_pipeline():
    # Connect to the database
    conn = sqlite3.connect(database)
    
    try:
        # Load CSV files
        customers_df = pd.read_csv(customers_file)
        orders_df = pd.read_csv(orders_file)
        
        # Perform any necessary data transformations
        # Example: rename columns, handle missing values, etc.
        
        # Load data into SQLite tables
        load_to_sqlite(customers_df, 'customers', conn)
        load_to_sqlite(orders_df, 'orders', conn)
        
        print("Data pipeline completed successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

# Run the pipeline
run_pipeline()
