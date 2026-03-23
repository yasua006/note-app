import mariadb

from modules.config import db_name, db_config

from asgiref.wsgi import WsgiToAsgi
# from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, jsonify

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

# def insert_note(cursor, title: str, description: str) -> None:
#     app.logger.info("Inserting rows...")

#     insert_query = "INSERT INTO Notes (title, description) VALUES (?, ?)"

#     # parametized (?) - no SQL injection attack
#     cursor.execute(insert_query, (title, description))
#     app.logger.info(f"Row count inserted: {cursor.rowcount}")

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
    return jsonify("/add is down. Coming back soon..."), 503

    # title: str | None = request.form.get("title")
    # description: str | None = request.form.get("description")
    
    # # log_file.write(f"tittel og beskrivelse: {title, description}\n")

    # response = handle_empty_note(title=title, description=description)
    # if response: return response

    # # log_file.write("før notat dict\n")

    # index: str = hashlib.sha512().hexdigest()

    # note: dict[str, dict[str, str | None]] = {
    #     f"note_{index}": {
    #         "title": title,
    #         "description": description
    #     }
    # }

    # # log_file.write(f"notat `dict`: {json.dumps(note)}\n")

    # try:
    #     with open("notes.json", "r+") as notes_json:
    #         # log_file.write("før json load (add)\n")
    #         # log_file.write(f"Stream posisjon før readlines: {str(notes_json.tell())}\n")
    #         notes = json.load(notes_json)
            
    #         # if not notes:
    #             # log_file.write("notater - tom\n")

    #         # log_file.write(f"notater før ny notat: {notes or "null"}\n")
    #         notes.update(note)
    #         # log_file.write(f"notater etter ny notat: {notes or "null"}\n")

    #         # log_file.write(f"Stream posisjon etter readlines: {str(notes_json.tell())}")

    #         # * Etter siste logg
    #         # log_file.close()

    #         notes_json.seek(0)
    #         json.dump(notes, notes_json, indent=4, separators=(",", ":"))
    # except FileNotFoundError as fnfe:
    #     app.logger.error("`notes.json` doesn't exist!", fnfe)
    #     return jsonify({"error": "notes.json doesn't exist!"}), 500
    # except json.JSONDecodeError as jde:
    #     app.logger.error("`notes.json` couldn't update!", jde)
    #     return jsonify({"error": "notes.json couldn't update!"}), 500
    # except Exception as ex:
    #     app.logger.error("Cannot add note!", ex)
    #     return jsonify({"error": "Cannot add note!"}), 500

    # return jsonify(note), 201

asgi_app: WsgiToAsgi = WsgiToAsgi(app)

if __name__ == "__main__":
    app.run()