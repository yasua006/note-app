def close_db(cursor, conn) -> None:
    if cursor:
        cursor.close()
    if conn:
        conn.close()