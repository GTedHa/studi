
from flask_restful import Api

from studi import app
from studi import sqlalchemy_orm

import csv

api = Api(app)

def save_csv_contents_to_db(file_name, note, Production=False):
    if not Production:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

    # Data model object
    Notes = sqlalchemy_orm.Notes
    Clauses = sqlalchemy_orm.Clauses
    ClausePoints = sqlalchemy_orm.ClausePoints

    note_id = sqlalchemy_orm.insert_data_to_db("Notes", Notes(file_name))
    for clauses_dict in note:
        title = None
        content = None
        for key, value in clauses_dict.items():
            if key == 'title': title = value
            if key == 'content': content = value
        clauses_id = sqlalchemy_orm.insert_data_to_db("Clauses", Clauses(note_id, title, content))
        sqlalchemy_orm.insert_data_to_db("ClausePoints", ClausePoints(clauses_id, note_id, 0, 0))
    return note_id


def insert_csv_to_db(Production=False):
    if not Production:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

    note_id = None
    with open('../studi/uploads/studi_test_file.csv') as csv_file:
        note = csv.DictReader(csv_file)
        note_id = save_csv_contents_to_db('studi_test_file', note)
    return note_id
