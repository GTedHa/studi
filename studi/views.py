from flask import render_template

from studi import app
from studi import intf_db


@app.route('/')
def index():
    return render_template('index.html')

"""
@app.route('/note/<int:note_id>')
def show_note_page(note_id):
    try:
        rv = intf_db.query_db(
            "SELECT note_name FROM Notes WHERE note_id={0}".format(note_id)
        )
    except Exception as exc:
        app.logger.warn("Exception raised during 'SELECT note_name FROM Notes WHERE note_id={0}' query: {1}".format(
            note_id, str(exc)
        ))
        return render_template('note.html', note_name='Wrong Note', note_id=note_id)
    if rv:
        try:
            item = rv[0]
            note_name = item['note_name']
        except Exception as exc:
            app.logger.warn(
                "Exception raised during access to query row item {0}: {1}".format(
                    item, str(exc)
                )
            )
            note_name = 'Wrong note'
    else:
        note_name = 'Note not found'
    return render_template('note.html', note_name=note_name, note_id=note_id)
"""

@app.route('/upload_test')
def upload_test():
    return render_template('file_test.html')