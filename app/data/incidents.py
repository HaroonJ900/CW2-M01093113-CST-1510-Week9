from app.data.db import connect_database
import pandas as pd


# adds a new cyber incident into the database
def insert_incident(date, title, severity, status, user_id):
    conn = connect_database()
    cursor = conn.cursor()
    sql = """
    INSERT INTO cyber_incidents (title, severity, status, date, user_id)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (title, severity, status, date, user_id))
    conn.commit()
    conn.close()


# retrieves all incidents sorted by newest first
def get_all_incidents():
    conn = connect_database()
    query = "SELECT * FROM cyber_incidents ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# fetches incidents that match a specific severity level
def get_incidents_by_severity(severity_level):
    conn = connect_database()
    query = "SELECT * FROM cyber_incidents WHERE severity = ? ORDER BY id DESC"
    df = pd.read_sql_query(query, conn, params=(severity_level,))
    conn.close()
    return df


# fetches incidents based on a specific status
def get_incidents_by_status(status):
    conn = connect_database()
    query = "SELECT * FROM cyber_incidents WHERE status = ? ORDER BY id DESC"
    df = pd.read_sql_query(query, conn, params=(status,))
    conn.close()
    return df


# updates the status of a specific incident
def update_incident_status(incident_id, new_status):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )
    conn.commit()
    conn.close()


# deletes an incident by its ID
def delete_incident(incident_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    conn.close()


# groups incidents by title to count how many times each type occurred
def get_incidents_by_type_count():
    conn = connect_database()
    query = """
        SELECT title, COUNT(*) AS count
        FROM cyber_incidents
        GROUP BY title
        ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# counts how many high-severity incidents exist for each status
def get_high_severity_by_status():
    conn = connect_database()
    query = """
        SELECT status, COUNT(*) AS count
        FROM cyber_incidents
        WHERE severity = 'High'
        GROUP BY status
        ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# gets incident types that appear more than a chosen number of times but greater than or equal to 5 
def get_incident_types_with_many_cases(min_count=5):
    conn = connect_database()
    query = """
        SELECT title, COUNT(*) AS count
        FROM cyber_incidents
        GROUP BY title
        HAVING COUNT(*) > ?
        ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    conn.close()
    return df

# retrieves one specific incident using its ID
def get_incident_by_id(incident_id):
    conn = connect_database()
    query = "SELECT * FROM cyber_incidents WHERE id = ?"
    df = pd.read_sql_query(query, conn, params=(incident_id,))
    conn.close()
    return df
