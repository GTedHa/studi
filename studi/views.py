
from flask import render_template
from studi import app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes/<note_id>')
def show_note_page(note_id):
    return render_template('note.html', note_id=note_id)


@app.route('/upload_test')
def upload_test():
    return render_template('file_test.html')
