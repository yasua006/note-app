from typing import Literal, LiteralString

T_To_Patch = Literal["Notes", "TODOs"]


def handle_patch_query(t_to_patch: T_To_Patch, task_done: int | None = None) -> LiteralString:
    patch_query = ""

    if task_done:
        patch_query = f"UPDATE {t_to_patch} SET title = ?, description = ?, task_done = ? WHERE id = ? AND user_id = ?"
    else:
        patch_query = f"UPDATE {t_to_patch} SET title = ?, description = ? WHERE id = ? AND user_id = ?"

    return patch_query

def handle_patch_execution(cursor, patch_query: LiteralString,
    title: str, description: str,
    row_id: int, user_id: int, task_done: int | None) -> None:
    
    if task_done is None:
        cursor.execute(patch_query, (title, description, row_id, user_id))
    else:
        cursor.execute(patch_query, (title, description, task_done, row_id, user_id))

def patch_row(cursor, t_to_patch: T_To_Patch,
    title: str, description: str,
    row_id: int, user_id: int, task_done: int | None = None) -> None:

    patch_query: LiteralString = handle_patch_query(t_to_patch, task_done)
    handle_patch_execution(cursor=cursor, patch_query=patch_query,
        title=title, description=description,
        row_id=row_id, user_id=user_id, task_done=task_done)
