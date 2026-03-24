from typing import Literal

Show_What = Literal["Notes", "TODOs"]


def select_all_db(cursor, show_what: Show_What):
    select_query = f"SELECT * FROM {show_what}"
    cursor.execute(select_query)
    return cursor.fetchall()