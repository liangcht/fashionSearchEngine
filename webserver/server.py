import sqlite3
import os
import base64
import sys
import numpy as np
import json
import color_hist_test
import type_classification
import dct_99
from flask import Flask, g, render_template, request, url_for, redirect
from flask.ext.images import resized_img_src
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
from sets import Set
from decimal import Decimal
import math

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

        # Compute the distance for query image
        query_path = 'static/uploads/' + filename
        CNN_result = type_classification.getCNNresult(query_path)
        global CNN_dist 
        CNN_dist = CNN_result[0]
        global col_dist 
        col_dist = color_hist_test.colDistance(3, query_path)
        global DCT_dist
        DCT_dist = dct_99.DCTDistance(query_path)
        global query_type_result
        query_type_result  = CNN_result[1]
        global cnn_ft 
        cnn_ft = CNN_result[2]
        
        return "success"
    except:
        print("error when saving cropped imgage")
        return "error"

    

@app.route('/file_result', methods=['GET','POST'])
def find_result():
    try:
        weight1 = float(request.form['w1'])/10.0 # get color/type weight
        weight3 = int(request.form['w3'])
        filename = request.form['name']
        mode = request.form['mode']
        win_size = int(20 + (math.pow(2, weight3)-1)/(math.pow(2,9))*28522) #window size
        #idset_querydata = type_classification.getNeighbor_fine(fac, win_size, 'static/uploads/'+filename)
        print(win_size)
        winner = list(CNN_dist.argsort()[:win_size])
        total_score = weight1 * DCT_dist + (1 - weight1) * col_dist
        selected_score_pair = [(total_score[id], id) for id in winner]
        selected_score_pair.sort()
        final_winner = [selected_score_pair[i][1] for i in xrange(20)]
        final_winner_scores = [selected_score_pair[i][0] for i in xrange(20)]

        db = get_db()
        result = []
        scoreSet = set() # get unique image results
        selected_id = []
        for index, _id_ in enumerate(final_winner):
            rst = db.execute(
                'SELECT name, gender, type, source, path FROM amazon WHERE id = ?', (_id_, )
            ).fetchone()
            if round(final_winner_scores[index], 6) not in scoreSet:
                result.append(rst)
                scoreSet.add(round(final_winner_scores[index], 6))
                selected_id.append(_id_)
            if len(result) >= 10:
                break
        print (final_winner_scores)

        #top_ctg = open("category_label.txt").readlines()
        top_ctg = open("ACS_label.txt").readlines()

        pic_data = []
        top_colors = []
        for _id_ in selected_id:
            col = cnn_ft[_id_].argsort()[::-1][:3]
            col_score = []
            for c in col:
                col_score.append(( top_ctg[c], round(cnn_ft[_id_][c], 2) )) 
            pic_data.append(col_score)

        # for debug
        #####
        #idset_querydata = range(2)
        #idset_querydata[0] = range(1, 11)
        #idset_querydata[1] = ((1,1), (1,1),(1,1),(1,1),(1,1))
        ###

        entries = [dict(name=row[0], gender=row[1], type=row[2], source=row[3], path="/crawlImages_large/" + row[4]) for row in result]
        if (mode == '0'):
            print("render upload")
            return render_template('upload.html', entries=entries, filename=filename, pic_data=pic_data, querydata=query_type_result)
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
