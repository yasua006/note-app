from typing import Literal

T_To_Delete = Literal["Users", "Notes", "TODOs"]


def delete_row(cursor, t_to_delete: T_To_Delete, row_id: int, user_id: int) -> None:
    delete_query = f"DELETE FROM {t_to_delete} WHERE id = ? AND user_id = ?"
    cursor.execute(delete_query, (row_id, user_id))
