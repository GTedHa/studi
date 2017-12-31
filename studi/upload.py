import os
import xml.etree.ElementTree as ElementTree

from flask import request
from flask_restful import Resource, Api, reqparse
import werkzeug
from werkzeug.utils import secure_filename

import studi
from studi import app
from studi import module_path

DIRPATH = module_path + '/uploads/'
api = Api(app)

class UploadMaterial(Resource):

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('studi_material', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        material = args['studi_material']
        filepath = DIRPATH + secure_filename(material.filename)
        material.save(filepath)
        if save_contents_to_db(filepath):
            return { 'result': True }, 200
        else:
            return { 'result': False }, 400

api.add_resource(UploadMaterial, '/upload')

def save_contents_to_db(filepath):
    result = False
    try:
        db = studi.intf_db.get_db()
        tree = ElementTree.parse(filepath)
        note = tree.getroot()
        note_name = note.attrib['name']
        ins_note_qry = "INSERT INTO Notes(note_name) VALUES('{0}')".format(note_name)
        note_id = studi.intf_db.insert_db(ins_note_qry)
        for item in note:
            title = item.attrib['title']
            content = item.text
            ins_clause_qry = "INSERT INTO Clauses(note_id, title, contents) VALUES({0}, '{1}', '{2}')".format(
                note_id, title, content
            )
            clause_id = studi.intf_db.insert_db(ins_clause_qry)
            ins_points_qry = "INSERT INTO ClausePoints(clause_id, note_id, imp, und) VALUES({0}, {1}, {2}, {3})".format(
                clause_id, note_id, 0, 0
            )
            studi.intf_db.insert_db(ins_points_qry)
            result = True
    except Exception as exc:
        # TODO: more elegant exception handling..
        app.logger.warn("Exception raised during DB insertions: {0}".format(str(exc)))
    os.remove(filepath)
    return result
