from modules.select_db import select_all_db


def create_todos(cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TODOs(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            task_done BOOLEAN NOT NULL
        )
    """)

def insert_todo(cursor, user_id: int, title: str, description: str, task_done: str):
    insert_query = "INSERT INTO TODOs (user_id, title, description, task_done) VALUES (?, ?, ?, ?)"

    # parametized (?) - no SQL injection attack
    cursor.execute(insert_query, (user_id, title, description, task_done))
    return cursor.lastrowid

def get_todos(cursor, user_id: int):
    return select_all_db(cursor, "TODOs", user_id)
