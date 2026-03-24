from modules.select_db import select_all_db


def create_notes(cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notes(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL
        )
    """)

def insert_note(cursor, title: str, description: str):
    insert_query = "INSERT INTO Notes (title, description) VALUES (?, ?)"

    # parametized (?) - no SQL injection attack
    cursor.execute(insert_query, (title, description))
    return cursor.lastrowid

def get_notes(cursor):
    return select_all_db(cursor, "Notes")