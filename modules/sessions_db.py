def create_sessions(cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sessions(
            session_id VARCHAR(255) PRIMARY KEY,
            user_id INT NOT NULL
        )
    """)

def insert_session(cursor, session_id: str, user_id: int):
    insert_query = "INSERT INTO Sessions (session_id, user_id) VALUES (?, ?)"
 
    # parametized (?) - no SQL injection attack
    cursor.execute(insert_query, (session_id, user_id))

def is_user_logged_in(cursor, session_id: str):
    select_query = "SELECT user_id FROM Sessions WHERE session_id = ?"

    cursor.execute(select_query, [session_id])
    row = cursor.fetchone()

    if row is None:
        return False

    return row["user_id"]
