from app.data.db import connect_database
import pandas as pd


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


def get_all_incidents():
    conn = connect_database()
    query = "SELECT * FROM cyber_incidents ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_incidents_by_severity(severity_level):
    conn = connect_database()
    query = "SELECT * FROM cyber_incidents WHERE severity = ? ORDER BY id DESC"
    df = pd.read_sql_query(query, conn, params=(severity_level,))
    conn.close()
    return df


def get_incidents_by_status(status):
    conn = connect_database()
    query = "SELECT * FROM cyber_incidents WHERE status = ? ORDER BY id DESC"
    df = pd.read_sql_query(query, conn, params=(status,))
    conn.close()
    return df


def update_incident_status(incident_id, new_status):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )
    conn.commit()
    conn.close()


def delete_incident(incident_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    conn.close()


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
