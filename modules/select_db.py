def select_all_db(cursor):
    select_query = "SELECT * FROM Notes"
    cursor.execute(select_query)
    return cursor.fetchall()