import sqlite3
from flask import Flask, g, render_template, request
from flask.ext.images import resized_img_src

app = Flask(__name__, static_url_path = "", static_folder = "static")
SQLITE_DB_PATH = '../amazon/test.db'
# SQLITE_DB_SCHEMA = '../amazon/try_db.sql'


# SQLite3-related operations
# See SQLite3 usage pattern from Flask official doc
# http://flask.pocoo.org/docs/0.10/patterns/sqlite3/
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/chooseType', methods=['POST'])
def chooseType():
    # Get the database connection
    db = get_db()
    type_name = request.form.get('type')
    # valid_ids = [row[0] for row in cursor]
    result = db.execute(
        'SELECT type, path, id FROM amazon WHERE type = ?', (type_name, )
    )
    entries = [dict(type=row[0], path=row[1].replace("/Users/tj474474/Development/visual_database/amazon/crawlImages", "/sample_image"), id=row[2]) for row in result.fetchall()]
    return render_template('another.html', entries=entries)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)