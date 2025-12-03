import pandas as pd 
from app.data.db import connect_database 

# adds a new dataset record into the database and returns its ID
def insert_dataset(name ,source, category, size):
    conn = connect_database()
    cursor = conn.cursor()
    query = """
    INSERT INTO datasets_metadata (name, source, category, size) 
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (name, source, category, size))
    conn.commit()
    dataset_id =cursor.lastrowid
    conn.close()
    return dataset_id
    

# retrieves all datasets sorted from newest to oldest
def get_all_datasets():
    conn = connect_database()
    query = "SELECT * FROM datasets_metadata ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df 

# deletes a dataset using its ID
def delete_a_dataset(dataset_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?",(dataset_id,))
    conn.commit()
    conn.close()

# returns the dataset record that matches the given ID
def get_dataset_by_id(dataset_id):
    conn = connect_database()
    query = "SELECT * FROM datasets_metadata WHERE id = ?"
    df = pd.read_sql_query(query, conn, params=(dataset_id,))
    conn.close()
    return df
