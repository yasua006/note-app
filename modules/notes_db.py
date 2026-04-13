from modules.select_db import select_all_db


def create_notes(cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notes(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL
        )
    """)

def insert_note(cursor, user_id: int, title: str, description: str):
    insert_query = "INSERT INTO Notes (user_id, title, description) VALUES (?, ?, ?)"

    # parametized (?) - no SQL injection attack
    cursor.execute(insert_query, (user_id, title, description))
    return cursor.lastrowid

def get_notes(cursor, user_id: int):
    return select_all_db(cursor, "Notes", user_id)
