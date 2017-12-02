from flask import render_template

from studi import app


@app.route('/')
def index():
    app.logger.warning('sample message')
    return render_template('index.html')

@app.route('/note/<int:note_id>')
def show_note_page(note_id):
    note_name = 'Temp note'
    return render_template('note.html', note_name=note_name)

