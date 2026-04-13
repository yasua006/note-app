from typing import Literal

Show_What = Literal["Notes", "TODOs"]


def select_all_db(cursor, show_what: Show_What, user_id: int):
    select_query = f"SELECT * FROM {show_what} WHERE user_id = ?"
    cursor.execute(select_query, [user_id])
    return cursor.fetchall()
