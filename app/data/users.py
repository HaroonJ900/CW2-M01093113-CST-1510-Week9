from app.data.db import connect_database 

# inserts a new user into the database and returns the new user's ID
def insert_user(username, hash_password, role='user'):
    conn = connect_database()
    cursor = conn.cursor 
    conn.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?,)
    """, (username, hash_password, role))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

# searches for a user by their username
def find_user_by_username(username):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users WHERE username = ?
        """, (username,))
    user = cursor.fetchone()
    conn.close()
    return user
