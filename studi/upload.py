from bs4 import BeautifulSoup
from flask import request
from flask_restful import Resource, Api

from studi import app
from studi import module_path
from studi import sqlite_db

import csv
DIRPATH = module_path + '/uploads/'

api = Api(app)

class UploadCSVMaterial(Resource):

    def post(self):
        try:
            file_name = request.files['studi_material'].filename

            # Cross-site scripting (XSS)
            if file_name[-3:] != "csv":
                app.logger.warn(
                    "Exception raised during upload new file file name is : {0}".format(file_name))
                return {'result' : False, \
                        'description' : "file's extenstion is not .csv. You should upload csv file. \
                        Uploaded file name is : {0}".format(file_name)}, 400


            temp = request.files['studi_material']
            csvfile = temp.read().decode("utf-8").splitlines()
            note = csv.DictReader(csvfile)
            if save_csv_contents_to_db(file_name[:-3], note, True):
                return {'result': True}, 200
            else:
                return {'result': False}, 400
        except Exception as e:
            print(e)

# api.add_resource(UploadCSVMaterial, '/upload')

def save_csv_contents_to_db(file_name, note, Production=False):
    if Production:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/studi.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

    # Data model object
    Note = sqlite_db.Note
    Clauses = sqlite_db.Clauses
    ClausePoints = sqlite_db.ClausePoints
    try:
        note_id = sqlite_db.insert_data_to_db("Note", Note(file_name))
        for clauses_dict in note:
            title = None
            content = None
            for key, value in clauses_dict.items():
                if key == 'title': title = value
                if key == 'content': content = value
            clauses_id = sqlite_db.insert_data_to_db("Clauses", Clauses(note_id, title, content))
            sqlite_db.insert_data_to_db("ClausePoints", ClausePoints(clauses_id, note_id, 0, 0))
    except Exception as exc:
        # TODO: more elegant exception handling..
        app.logger.warn(
            "Exception raised during DB insertions: {0}".format(exc))
    else:
        return note_id


def insert_csv_to_db(Production=False):
    if Production:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/studi.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

    note_id = None
    with open('../studi/uploads/studi_test_file.csv') as csv_file:
        note = csv.DictReader(csv_file)
        note_id = save_csv_contents_to_db('studi_test_file', note)
    return note_id


if __name__ == "__main__":
    insert_csv_to_db()
