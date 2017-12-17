from flask import request, jsonify, Response
from flask_restful import reqparse, Api, Resource

from studi import app
from studi import intf_db

api = Api(app)

class Notes(Resource):

    def __init__(self):
        pass

    def post(self):
        try:
            rv = intf_db.query_db(
                "SELECT * FROM Notes"
            )
        except Exception as exc:
            logger.warn("Exception raised during 'SELECT * FROM Notes;' query: {0}".format(
                str(exc)
            ))
            return { 'notes': None }, 500
        if rv:
            notes = []       
            for item in rv:
                note = dict()
                for key in item.keys():
                    note[key] = item[key]
                notes.append(note)
            return { 'notes': notes }, 200
        else:
            return { 'notes': None }, 201


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



class Clause(Resource):

    def __init__(self):
        pass

    def put(self):
        app.logger.debug('PUT /clause/update requested')
        parser = reqparse.RequestParser()
        parser.add_argument('clause_id', type=int, required=True, location='json')
        parser.add_argument('imp', type=int, required=True, location='json')
        parser.add_argument('und', type=int, required=True, location='json')
        args = parser.parse_args()
        # TODO: update DB
        # log debug
        app.logger.debug('clause_id: {0}'.format(args['clause_id']))
        app.logger.debug('imp: {0}'.format(args['imp']))
        app.logger.debug('und: {0}'.format(args['und']))
        return { 'result': True }, 200


api.add_resource(Notes, '/notes')
api.add_resource(Clauses, '/clauses/list')
api.add_resource(Clause, '/clause/update')
