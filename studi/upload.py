from bs4 import BeautifulSoup
from flask import request
from flask_restful import Resource, Api

from studi import app
from studi import module_path
from studi import sqlalchemy

import csv
DIRPATH = module_path + '/uploads/'

api = Api(app)

def save_csv_contents_to_db(file_name, note, Production=False):
    if not Production:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

    # Data model object
    Notes = sqlalchemy.Notes
    Clauses = sqlalchemy.Clauses
    ClausePoints = sqlalchemy.ClausePoints
    try:
        note_id = sqlalchemy.insert_data_to_db("Notes", Notes(file_name))
        for clauses_dict in note:
            title = None
            content = None
            for key, value in clauses_dict.items():
                if key == 'title': title = value
                if key == 'content': content = value
            clauses_id = sqlalchemy.insert_data_to_db("Clauses", Clauses(note_id, title, content))
            sqlalchemy.insert_data_to_db("ClausePoints", ClausePoints(clauses_id, note_id, 0, 0))
    except Exception as exc:
        # TODO: more elegant exception handling..
        app.logger.warn(
            "Exception raised during DB insertions: {0}".format(exc))
    else:
        return note_id


def insert_csv_to_db(Production=False):
    if not Production:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

    note_id = None
    with open('../studi/uploads/studi_test_file.csv') as csv_file:
        note = csv.DictReader(csv_file)
        note_id = save_csv_contents_to_db('studi_test_file', note)
    return note_id
