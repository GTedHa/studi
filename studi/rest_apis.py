from flask import request, jsonify, Response
from flask_restful import Api, Resource

from studi import app

api = Api(app)

class Notes(Resource):

    def __init__(self):
        pass

    def post(self):
        dummys = []
        for i in range(0, 3):
            dummy = {
                'note_id': 100+i,
                'note_name': 'Note {0}'.format(i+1)
            }
            dummys.append(dummy)
        return { 'notes': dummys }, 200

api.add_resource(Notes, '/notes/list')
