import sqlite3
import os
import base64
import sys
from binascii import a2b_base64
import type_classification
from flask import Flask, g, render_template, request, url_for, redirect
from flask.ext.images import resized_img_src
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
from sets import Set

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


@app.route('/upload_img', methods=['GET', 'POST'])
def upload_img():
    img = request.form['img'] + "=="
    decode_img = img.decode("base64")
    try:
        fd = open('static/uploads/test.png', 'w')
        fd.write(decode_img)
        fd.close()
        return render_template('upload.html', entries=[], filename='/uploads/g1.png')
    except:
        return render_template('index.html', entries=[dict(error='invalid image type.')])

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            idset = type_classification.getNeighbor('static/uploads/'+filename)
            # for debug
            # idset = range(1, 11)
            db = get_db()
            result = []
            nameSet = set()
            for _id_ in idset:
                rst = db.execute(
                    'SELECT name, gender, type, source, path FROM amazon WHERE id = ?', (_id_, )
                ).fetchone()
                if rst[0] not in nameSet:
                    result.append(rst)
                    nameSet.add(rst[0])
                if len(result) >= 10:
                    break
            entries = [dict(name=row[0], gender=row[1], type=row[2], source=row[3], path=row[4].replace("/Users/tj474474/Development/visual_database/amazon", "")) for row in result]
            return render_template('upload.html', entries=entries, filename=filename)
    return render_template('index.html', entries=[dict(error='invalid image type.')]) 

@app.route('/chooseType', methods=['POST'])
def chooseType():
    # Get the database connection
    db = get_db()
    type_name = request.form.get('type')
    # valid_ids = [row[0] for row in cursor]
    result = db.execute(
        'SELECT type, path, id FROM amazon WHERE type = ? LIMIT 10', (type_name, )
    )
    entries = [dict(type=row[0], path=row[1].replace("/Users/tj474474/Development/visual_database/amazon", ""), id=row[2]) for row in result.fetchall()]
    return render_template('result.html', entries=entries)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)