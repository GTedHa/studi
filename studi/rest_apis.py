from flask import request, jsonify, Response
from flask_restful import reqparse, Api, Resource

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

class Clauses(Resource):

    def __init__(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('note_id', type=int, help='Note ID')
        args = parser.parse_args()
        note_id = args['note_id']
        dummys = []
        for i in range(0, 10):
            dummy = {
                'clause_id': 10+i,
                'title': 'Clause {0}'.format(i+1),
                'contents': 'Clause {0} means nothing...'.format(i+1),
                'imp': 0,
                'und': 1
            }
            dummys.append(dummy)
        return { 'note_id': note_id, 'clauses': dummys }, 200

api.add_resource(Clauses, '/clauses/list')
