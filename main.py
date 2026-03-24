import mariadb

from modules.config import db_name, db_config

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, render_template, request, jsonify

app: Flask = Flask(__name__)

log_file = open("log.txt", "a+")
log_file.seek(0)


def create_notes(cursor) -> None:
    app.logger.info(f"Connected to database {db_name}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notes(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL
        )
    """)
    app.logger.info("Executed creation of Notes")

def insert_note(cursor, title: str, description: str):
    app.logger.info("Inserting rows...")

    insert_query = "INSERT INTO Notes (title, description) VALUES (?, ?)"

    # parametized (?) - no SQL injection attack
    cursor.execute(insert_query, (title, description))
    app.logger.info(f"Row count inserted: {cursor.rowcount}")
    return cursor.lastrowid

def get_notes(cursor):
    select_query = "SELECT * FROM Notes"
    cursor.execute(select_query)
    return cursor.fetchall()

def close_db(cursor, conn) -> None:
    if cursor:
        cursor.close()
        app.logger.info("Closed cursor")
    if conn:
        conn.close()
        app.logger.info("Closed connection")

@app.route("/")
def home() -> str | None:
    cursor = None
    conn = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        create_notes(cursor)
        notes = get_notes(cursor)

        return render_template("index.html", notes=notes)
    except mariadb.Error as err:
        app.logger.info("Data handling failed!", err)
        conn.rollback()
    finally:
        close_db(cursor=cursor, conn=conn)

# TODO: Håndtere tom notater (neste commit)
@app.route("/notes", methods=["GET"])
def show_all_notes():
    cursor = None
    conn = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        log_file.write("\n–––––––––––––––––––––––––––––––––––\n\n")
        log_file.write("Før select query - alle notes\n")
        notes = get_notes(cursor)
        log_file.write(f"Notater: {notes}")

        return jsonify(notes), 200
    except mariadb.Error as err:
        app.logger.info("Data handling failed!", err)
        conn.rollback()
    finally:
        close_db(cursor=cursor, conn=conn)

def handle_empty_note(title: str | None, description: str | None):
    if not title or not description:  # reason: terminal users
        note: dict[str, str] = {
            "error": "Title or description - empty!"
        }

        return jsonify(note), 400

@app.route("/add", methods=["POST"])
def add_note():
    cursor = None
    conn = None

    title: str | None = request.form.get("title")
    description: str | None = request.form.get("description")

    # log_file.write(f"tittel og beskrivelse: {title, description}\n")

    response = handle_empty_note(title=title, description=description)
    if response: return response

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        note_id = insert_note(cursor=cursor, title=title, description=description)
        
        # if not note:
            # log_file.write("notater - tom\n")

        # log_file.write(f"notater før ny notat: {notes or "null"}\n")
        # log_file.write(f"notater etter ny notat: {notes or "null"}\n")
        return jsonify(f"Note with id {note_id} successfully created"), 201
    except mariadb.Error as err:
        app.logger.info("Data insert failed!", err)
        conn.rollback()
    except Exception as ex:
        app.logger.error("Cannot add note!", ex)
        return jsonify({"error": "Cannot add note!"}), 500
    finally:
        close_db(cursor=cursor, conn=conn)

asgi_app: WsgiToAsgi = WsgiToAsgi(app)

if __name__ == "__main__":
    app.run()