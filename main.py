import mariadb

from modules.config import db_config
from modules.notes_db import *
from modules.close_db import close_db

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, render_template, request, jsonify

app: Flask = Flask(__name__)

log_file = open("log.txt", "a+")
log_file.seek(0)
log_file.write("\n–––––––––––––––––––––––––––––––––––\n\n")


@app.route("/")
def home() -> str | None:
    cursor = None
    conn = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        create_notes(cursor)
        notes = get_notes(cursor)

        # for item in notes:
            # log_file.write(f"Notat values vist: {item.values()}\n")
            # log_file.write(f"Notat tittel vist: {item["title"]}\n")
            # log_file.write(f"Notat beskrivelse vist: {item["description"]}\n")

        return render_template("index.html", notes=notes)
    except mariadb.Error as err:
        log_file.write(f"Data handling failed! {err}\n")
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

        log_file.write("Før select query - alle notes\n")
        notes = get_notes(cursor)

        log_file.write(f"Notater: {notes}\n")

        return jsonify(notes), 200
    except mariadb.Error as err:
        log_file.write(f"Data handling failed! {err}\n")
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

    log_file.write(f"tittel og beskrivelse: {title, description}\n")

    response = handle_empty_note(title=title, description=description)
    if response: return response

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        note_id = insert_note(cursor=cursor, title=title, description=description)

        return jsonify(f"Note with id {note_id} successfully created"), 201
    except mariadb.Error as err:
        log_file.write(f"Data insert failed! {err}")
        conn.rollback()
    except Exception as ex:
        app.logger.error("Cannot add note!", ex)
        return jsonify({"error": "Cannot add note!"}), 500
    finally:
        close_db(cursor=cursor, conn=conn)

asgi_app: WsgiToAsgi = WsgiToAsgi(app)

if __name__ == "__main__":
    app.run()