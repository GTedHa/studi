
from flask_restful import reqparse, Api, Resource
from studi import sqlite_db
from studi import app
from studi import intf_db
from studi.sqlite_db import Note, Clauses, ClausePoints

api = Api(app)


class Notes(Resource):
    def __init__(self):
        pass

    def post(self):
        try:
            result = sqlite_db.get_all_data_from_db(Note)
        except Exception as exc:
            app.logger.warn("Exception raised during 'Get date from Notes; {0}".format(str(exc)))
            return {'notes' : None}, 500

        if result:
            notes = []
            for item in result:
                note = dict()
                for name in Note.column:
                    note[name] = getattr(item, name)
                notes.append(note)
            return {'notes' : notes}, 200
        else:
            return {'notes' : None}, 201


class ClausePoints(Resource):

    def __init__(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('note_id', type=int, required=True)
        args = parser.parse_args()
        note_id = args['note_id']
        try:
            rv = intf_db.query_db(
                "SELECT * FROM ClausePoints WHERE note_id={0}".format(note_id)
            )
        except Exception as exc:
            app.logger.warn(
                "Exception raised during 'SELECT * FROM ClausePoints WHERE note_id={0}' query: {1}".format(
                    note_id, str(exc)
                )
            )
            return { 'note_id': note_id, 'clause_points': None }, 500
        if rv:
            clause_points = []
            for item in rv:
                point = dict()
                for key in item.keys():
                    if key != 'note_id':
                        point[key] = item[key]
                clause_points.append(point)
            return { 'note_id': note_id, 'clause_points': clause_points }, 200
        else:
            return { 'note_id': note_id, 'clause_points': None }, 201
                

class Clause(Resource):

    def __init__(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('clause_id', type=int, required=True)
        args = parser.parse_args()
        clause_id = args['clause_id']
        try:
            rv = intf_db.query_db(
                "SELECT * FROM Clauses WHERE clause_id={0}".format(clause_id)
            )
        except Exception as exc:
            app.logger.warn(
                "Exception raised during 'SELECT * FROM Clauses WHERE clause_id={0}' query: {1}".format(
                    clause_id, str(exc)
                )
            )
            return { 'clause_id': clause_id, 'title': None, 'contents': None }, 500
        if rv:
            try:
                item = rv[0]
                title = item['title']
                contents = item['contents']
                return { 'clause_id': clause_id, 'title': title, 'contents': contents }, 200
            except Exception as exc:
                app.logger.warn(
                    "Exception raised during access to query row item {0}: {1}".format(
                        item, str(exc)
                    )
                )
                return { 'clause_id': clause_id, 'title': None, 'contents': None }, 500
        else:
            return { 'clause_id': clause_id, 'title': None, 'contents': None }, 201


class UpdatePoint(Resource):

    def __init__(self):
        pass

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('clause_id', type=int, required=True)
        parser.add_argument('imp', type=int, required=True)
        parser.add_argument('und', type=int, required=True)
        args = parser.parse_args()
        clause_id = args['clause_id']
        imp = args['imp']
        und = args['und']
        query_statement = \
            "UPDATE ClausePoints SET imp={0}, und={1} WHERE clause_id={2}".format(
                imp, und, clause_id
            )
        try:
            rowcount = intf_db.update_db(query_statement, commit=True)
        except Exception as exc:
            app.logger.warn("{0} query: {1}".format(
                    query_statement, str(exc)
                )
            )
            return { 'result': False }, 500
        if rowcount != 1:
            return { 'result': False }, 201
        return { 'result': True }, 200


class DeleteNote(Resource):

    def __init__(self):
        pass

    def delete(self):
        # TODO: Delete Cluases and ClausePoints related to the note ID.
        parser = reqparse.RequestParser()
        parser.add_argument('note_id', type=int, required=True)
        args = parser.parse_args()
        note_id = args['note_id']
        query_statement = \
            "DELETE FROM Notes WHERE note_id = {0}".format(
                note_id
            )
        try:
            rowcount = intf_db.update_db(query_statement, commit=True)
        except Exception as exc:
            app.logger.warn("{0} query: {1}".format(
                    query_statement, str(exc)
                )
            )
            return { 'result': False }, 500
        if rowcount != 1:
            return { 'result': False }, 201
        return { 'result': True }, 200


api.add_resource(Notes, '/notes')
api.add_resource(ClausePoints, '/points')
api.add_resource(Clause, '/clause')
api.add_resource(UpdatePoint, '/point/update')
api.add_resource(DeleteNote, '/note/delete')
