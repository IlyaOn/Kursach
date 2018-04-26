from flask import render_template, request, flash, redirect, url_for, send_from_directory
from app import app, TF_ADAPT
from app.TF_ADAPT import calc_new_music
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['mp3', 'wav'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print(1)
    print (send_from_directory(app.config['UPLOAD_FOLDER'], filename))
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/index', methods=['GET', 'POST'])  
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('style' not in request.files) or ('music' not in request.files):
            flash('No file part')
            return redirect(request.url)
        style = request.files['style']
        music = request.files['music']
        # if user does not select file, browser also
        # submit a empty part without filename
        if style.filename == '' or music.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if style and allowed_file(style.filename) and music and allowed_file(music.filename):
            music.save(os.path.join(app.config['UPLOAD_FOLDER'], "music.mp3"))
            style.save(os.path.join(app.config['UPLOAD_FOLDER'], "style.mp3"))
            return redirect(url_for('uploaded_file',
                                    filename="style.mp3"))
    return render_template("index.html")
    