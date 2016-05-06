import sqlite3
import os
import base64
import sys
import numpy as np
import json
import color_hist_test
import type_classification
from flask import Flask, g, render_template, request, url_for, redirect
from flask.ext.images import resized_img_src
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
from sets import Set

SQLITE_DB_PATH = '../amazon/test_large_no_noise.db'
# SQLITE_DB_SCHEMA = '../amazon/try_db.sql'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
app = Flask(__name__, static_url_path = "", static_folder = "static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# SQLite3
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
    img = request.form['img']
    img = img.split(",", 1)[1]
    decode_img = base64.decodestring(img)
    filename = "test.jpg"
    try:
        fd = open('static/uploads/' + filename, 'w')
        fd.write(decode_img)
        fd.close()
        return "success"
    except:
        print("error when saving cropped imgage")
        return "error"

@app.route('/file_result', methods=['GET','POST'])
def find_result():
    try:
        factor = request.form['factor'] # get color/type weight
        filename = request.form['name']
        mode = request.form['mode']
        fac = float(factor) / 10.0
        idset_querydata = type_classification.getNeighbor_fine(fac, 'static/uploads/'+filename)

        # for debug
        #####
        #idset_querydata = range(2)
        #idset_querydata[0] = range(1, 11)
        #idset_querydata[1] = ((1,1), (1,1),(1,1),(1,1),(1,1))
        ###

        db = get_db()
        result = []
        scoreSet = set() # get unique image results
        idset = set()
        for index, _id_ in enumerate(idset_querydata[0]):
            rst = db.execute(
                'SELECT name, gender, type, source, path FROM amazon WHERE id = ?', (_id_, )
            ).fetchone()
            if idset_querydata[3][index] not in scoreSet:
                result.append(rst)
                scoreSet.add(idset_querydata[3][index])
                idset.add(_id_)
            if len(result) >= 10:
                break
        
        cnn_ft = np.load("crop_cnn_prob_large_fine.npy")
        top_ctg = open("category_label.txt").readlines()
        
        #hist = np.load("color_hist(crop).npy")

        pic_data = []
        for _index_ in idset_querydata[0]:
            if _index_ not in idset:
                continue
            #_index_ -= 1
            col = cnn_ft[_index_].argsort()[::-1][:5]
            col_score = []
            for c in col:
                col_score.append(( top_ctg[c], cnn_ft[_index_][c] )) 
            pic_data.append(col_score)

        # ave color
        print(idset_querydata[3])

        entries = [dict(name=row[0], gender=row[1], type=row[2], source=row[3], path="/crawlImages_large/" + row[4]) for row in result]
        if (mode == '0'):
            print("render upload")
            return render_template('upload.html', entries=entries, filename=filename, pic_data=pic_data, querydata=idset_querydata[1])
        elif (mode == '1'):
            print("render result")
            return render_template('result.html', entries=entries, pic_data=pic_data)
    except:
        print("error when rendering result")
        return render_template('index.html', entries=[dict(error='invalid image type.')])

""" get image type
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
"""

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
