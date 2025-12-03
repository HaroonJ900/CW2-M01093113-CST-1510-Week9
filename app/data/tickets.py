import pandas as pd 
from app.data.db import connect_database 

# adds a new IT support ticket into the database and returns its ID
def insert_ticket(title ,priority ,status ,created_date ,user_id):
    conn = connect_database()
    cursor = conn.cursor()
    query = '''
    INSERT INTO it_tickets (title ,priority ,status ,created_date ,user_id )
    Values (?, ?, ?, ?, ?)
    '''
    cursor.execute(query,(title ,priority ,status ,created_date ,user_id))
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id

# retrieves all tickets sorted from newest to oldest
def get_all_tickets():
    conn = connect_database()
    query = "SELECT * FROM it_tickets ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
    
# deletes a ticket using its ID
def delete_a_ticket(ticket_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE id = ?",(ticket_id,))
    conn.commit()
    conn.close()

# fetches a single ticket by its ID
def get_ticket_by_id(ticket_id):
    conn = connect_database()
    query = "SELECT * FROM it_tickets WHERE id = ?"
    df = pd.read_sql_query(query, conn, params=(ticket_id,))
    conn.close()
    return df
