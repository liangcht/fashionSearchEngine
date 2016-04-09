import sqlite3
import os
from flask import Flask, g, render_template, request, url_for, redirect
from werkzeug import secure_filename

SQLITE_DB_PATH = '../amazon/test.db'
# SQLITE_DB_SCHEMA = '../amazon/try_db.sql'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
app = Flask(__name__, static_url_path = "", static_folder = "static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload.html', filename=filename);
    return render_template('index.html', entries=[dict(error='invalid image type.')])

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
    return render_template('result.html', entries=entries)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)