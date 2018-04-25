from flask import render_template, request, flash, redirect, url_for, send_from_directory
from app import app
from app.TF_ADAPT import calc_new_music
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['mp3', 'wav'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.files)
        music = request.files['music']
        style = request.files['style']
        music_name = secure_filename(music.filename)
        style_name = secure_filename(style.filename)
        music.save(os.path.join(app.config['UPLOAD_FOLDER'], "music" ))
        style.save(os.path.join(app.config['UPLOAD_FOLDER'], "style"))
    return '''
    <head>
        <title>AAAAA</title>
    </head>
    <body>
    <form enctype="multipart/form-data">
        <h3>Выберите *.wav для адаптации</h3>
        <input type="file" name="music">
        <h3>Выберите *.wav со стилем</h3>
        <input type="file" name="style">
        <p><input type="submit" value="Adapt"></p>
    </form>
    </body>
    '''
    
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
    