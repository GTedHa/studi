import os
from bs4 import BeautifulSoup

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
        parse.add_argument(
            'studi_material',
            type=werkzeug.datastructures.FileStorage,
            location='files')
        args = parse.parse_args()
        material = args['studi_material']
        data = material.stream.read().decode('utf-8')
        if save_contents_to_db(data):
            return {'result': True}, 200
        else:
            return {'result': False}, 400


api.add_resource(UploadMaterial, '/upload')


def save_contents_to_db(data):
    result = False
    try:
        db = studi.intf_db.get_db()
        bs = BeautifulSoup(data)
        note = bs.find('note')
        note_name = note['name']
        ins_note_qry = "INSERT INTO Notes(note_name) VALUES(?)"
        note_id = studi.intf_db.insert_db(ins_note_qry, note_name)
        for item in bs.find_all('item'):
            title = item['title']
            title = title.replace("&", "&amp;")
            title = title.replace("<", "&lt;")
            title = title.replace(">", "&gt;")
            title = title.replace("\"", "&quot;")
            title = title.replace("\'", "&apos;")
            title = title.replace("\n", "<br/>")
            content = item.string
            content = content.replace("&", "&amp;")
            content = content.replace("<", "&lt;")
            content = content.replace(">", "&gt;")
            content = content.replace("\"", "&quot;")
            content = content.replace("\'", "&apos;")
            content = content.replace("\n", "<br/>")
            ins_clause_qry = \
                "INSERT INTO Clauses(note_id, title, contents) VALUES(?, ?, ?)"
            clause_id = \
                studi.intf_db.insert_db(
                    ins_clause_qry, note_id, title, content)
            ins_points_qry = \
                "INSERT INTO ClausePoints(clause_id, note_id, imp, und) VALUES(?, ?, ?, ?)"
            studi.intf_db.insert_db(ins_points_qry, clause_id, note_id, 0, 0)
            result = True
    except Exception as exc:
        # TODO: more elegant exception handling..
        app.logger.warn(
            "Exception raised during DB insertions: {0}".format(exc))
    return result
