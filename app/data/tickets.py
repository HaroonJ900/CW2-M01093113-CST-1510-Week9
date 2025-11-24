import pandas as pd 
from app.data.db import connect_database 

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
def get_all_tickets():
    conn = connect_database()
    query = "SELECT * FROM it_tickets ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
    
def delete_a_ticket(ticket_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE id = ?",(ticket_id,))
    conn.commit()
    conn.close()
