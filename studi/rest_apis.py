
from flask_restful import Api, Resource
from studi import sqlalchemy_orm
from studi import app
from flask import request, Response
from studi import upload
from studi import log
import csv

api = Api(app)

logger = log.gen_logger('studi')

class Note(Resource):

    def __init__(self):
        pass

    @log.logger_decorator_with_params(logger)
    def get(self, note_id=None):
        try:
            if note_id:
                result = sqlalchemy_orm.get_item_from_db(sqlalchemy_orm.Notes, {'note_id': note_id})
            else:
                result = sqlalchemy_orm.get_all_data_from_db(sqlalchemy_orm.Notes)
        except Exception as exc:
            app.logger.debug("Exception raised during 'GET date from Notes; {0}".format(str(exc)))
            return {'notes' : None}, 500
        else:
            if result:
                return {'notes' : result}, 200
            else:
                return {'notes' : result}, 201

    @log.logger_decorator_with_params(logger)
    def post(self):
        try:
            file = request.files['studi_material']
            file_name = file.filename.split('/').pop()

            # Cross-site scripting (XSS)
            if file_name[-3:] != "csv":
                app.logger.debug(
                    "Exception raised during upload new file file name is : {0}".format(file_name))
                return {'result' : False, \
                        'description' : "file's extenstion is not .csv. You should upload csv file. \
                        Uploaded file name is : {0}".format(file_name)}, 400

            request_file = request.files['studi_material']
            csvfile = request_file.read().decode("utf-8").splitlines()
            note = csv.DictReader(csvfile)
            if upload.save_csv_contents_to_db(file_name[:-4], note, True):
                return {'result': True}, 200
            else:
                return {'result': False}, 400
        except Exception as exc:
            app.logger.debug("Exception raised during POST note to Notes; {0}".format(str(exc)))
            return {'result' : False}, 500

    @log.logger_decorator_with_params(logger)
    def delete(self, note_id):
        try:
            sqlalchemy_orm.delete_note_and_related_data_from_db(int(note_id))
        except Exception as exc:
            app.logger.debug("Exception raised during Delete note from Notes; {0}".format(str(exc)))
            return {'result' : False}, 500
        else:
            # Todo ADD Verification Code
            return {'result': True}, 200

    @log.logger_decorator_with_params(logger)
    def put(self, note_id):
        new_note_name = request.form['new_note_name']
        try:
            sqlalchemy_orm.update_data_to_db(sqlalchemy_orm.Notes, {'note_id' : note_id}, {'note_name' : new_note_name})
        except Exception as exc:
            app.logger.debug("Exception raised during Delete note from Notes; {0}".format(str(exc)))
            return {'result' : False}, 500
        else:
            return {'result' : True}, 200




class Clause(Resource):
    def __init__(self):
        pass

    @log.logger_decorator_with_params(logger)
    def get(self, clause_id):
        try:
            result = sqlalchemy_orm.get_item_from_db(sqlalchemy_orm.Clauses, {'clause_id' : clause_id})
        except Exception as exc:
            app.logger.debug(
                "Exception raised during get data from clause ".format( clause_id, str(exc))
            )
            return { 'clause' }, 500
        if result:
                return {'clause' : result}, 200
        else:
            return {'clause' : result}, 201

    @log.logger_decorator_with_params(logger)
    def post(self):
        try:
            new_clause_id = sqlalchemy_orm.insert_data_to_db('Clauses', \
                                                             sqlalchemy_orm.Clauses(request.form['note_id'], \
                                                                                    request.form['title'], \
                                                                                    request.form['contents']))
        except Exception as exc:
            return {'clause_id' : None, 'title': None, 'contents' : None}, 500
        else:
            if new_clause_id:
                return {'clause_id' : new_clause_id, 'title' : request.form['title'], 'contents' : request.form['contents']}, 200
            else:
                return {'clause_id': None, 'title': None, 'contents': None}, 500

    @log.logger_decorator_with_params(logger)
    def delete(self, clause_id):
        try:

            result = sqlalchemy_orm.delete_data_from_db(sqlalchemy_orm.Clauses, {'clause_id' : clause_id})
        except Exception as exc:
            return {'clause_id': None}, 500
        else:
            if result:
                result = result[0]
                clause_id = getattr(result, 'clause_id')
                return {'clause_id': clause_id}, 200
            else:
                return {'clause_id': None}, 500

    @log.logger_decorator_with_params(logger)
    def put(self, clause_id):
        update_data = {}
        for key, value in request.form.items():
            update_data[key] = value

        try:
            clause = sqlalchemy_orm.update_data_to_db(sqlalchemy_orm.Clauses, {'clause_id' : clause_id}, update_data)
        except Exception as exc:
            return {'clause_id':clause_id, 'clause' : None}, 500
        else:
            if clause:
                return {'clause_id':clause_id, 'clause' : clause}, 200
            else:
                return {'clause_id':clause_id, 'clause' : clause}, 201



class ClausePoint(Resource):

    def __init__(self):
        pass

    @log.logger_decorator_with_params(logger)
    def get(self, **args):

        for key, value in request.args.items():
            args[key] = value

        try:
            result = sqlalchemy_orm.get_item_from_db(sqlalchemy_orm.ClausePoints, args)
        except Exception as exc:
            app.logger.debug(
                "Exception raised during 'SELECT * FROM ClausePoints WHERE args={0}' query: {1}".format(
                    args, str(exc)
                )
            )
            return {'note_id': args['note_id'], 'clause_points' : None}, 500
        else:
            if result:
                    return {'note_id': args['note_id'], 'clause_points': result}, 200
            else:
                return {'note_id': args['note_id'], 'clause_points' : result}, 201


    # 포인트 정보 업데이트
    @log.logger_decorator_with_params(logger)
    def put(self, clause_id):
        update_data = {}
        for key, value in request.form.items():
            update_data[key] = value
        try:
            clause_point = sqlalchemy_orm.update_data_to_db(sqlalchemy_orm.ClausePoints, {'clause_id' : clause_id}, update_data)
        except Exception as exc:

            app.logger.debug("Exception raised during 'Update point data to ClausePoints.\
            clause_id : {0}, update_data :{1}, error: {2}".format(clause_id, update_data, str(exc)))
            return {'clause_id' : clause_id, 'clause_point' : None}, 500
        else:
            if clause_point:
                return {'clause_id': clause_id, 'clause_point' : clause_point}, 200
            else:
                return {'clause_id': clause_id, 'clause_point': clause_point}, 201



api.add_resource(Note, '/api/notes','/api/notes/<note_id>')
api.add_resource(Clause, '/api/clauses', '/api/clauses/<clause_id>')
api.add_resource(ClausePoint, '/api/notes/<note_id>/clausePoints', '/api/clausePoints/<clause_id>')
