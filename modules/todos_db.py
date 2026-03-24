from modules.select_db import select_all_db


def create_todos(cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TODOs(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            task_done BOOLEAN NOT NULL
        )
    """)

def insert_todo(cursor, title: str, description: str, task_done: str):
    insert_query = "INSERT INTO TODOs (title, description, task_done) VALUES (?, ?, ?)"

    # parametized (?) - no SQL injection attack
    cursor.execute(insert_query, (title, description, task_done))
    return cursor.lastrowid

def get_todos(cursor):
    return select_all_db(cursor, "TODOs")