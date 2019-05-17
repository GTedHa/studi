
from flask_restful import Api, Resource
from werkzeug.exceptions import HTTPException
from studi import sqlalchemy_orm
from studi import app
from flask import request, Response
from studi import upload
from studi import log
from studi import custom_error
import sqlalchemy
from studi import util


import csv

api = Api(app)



class Note(Resource):

    def __init__(self):
        pass

    @log.logger_decorator_with_params(log.logger)
    def get(self):
        try:
            result = sqlalchemy_orm.get_all_data_from_db(sqlalchemy_orm.Notes)
        except sqlalchemy.exc.SQLAlchemyError:
            error_message = util.traceback_custom_error()
            response = custom_error.SQLAlchemyError(error_message).to_dict()
            return response, 500
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500
        else:
            if result:
                return {'notes' : result}, 200
            return {'notes': []}, 201


    @log.logger_decorator_with_params(log.logger)
    def post(self):
        try:
            request_file = request.files['studi_material']
            file_name = request_file.filename.split('/').pop()
        except HTTPException:
            error_message = util.traceback_custom_error()
            response = custom_error.HTTPRequestError(error_message).to_dict()
            return response, 400
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 400


        # Cross-site scripting (XSS)
        if file_name[-3:] != "csv":
            return custom_error.NotCSVFileError(file_name).to_dict(), 400

        try:
            csvfile = request_file.read().decode("utf-8").splitlines()
            # empty csv file
            if not csvfile:
                return custom_error.CSVError('csv file is empty'.format(csvfile)).to_dict(), 400
            note = csv.DictReader(csvfile)
        except csv.Error:
            error_message = util.traceback_custom_error()
            return custom_error.CSVError(error_message).to_dict(), 400

        try:
            new_note_id = upload.save_csv_contents_to_db(file_name[:-4], note, True)
        except sqlalchemy.exc.SQLAlchemyError:
            error_message = util.traceback_custom_error()
            response = custom_error.SQLAlchemyError(error_message).to_dict()
            return response, 500
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500
        else:
            return {'result': True}, 200



    @log.logger_decorator_with_params(log.logger)
    def delete(self, note_id):
        if isinstance(note_id, str):
            if not note_id.isdigit():
                return custom_error.BadRequestError().to_dict(), 400
            note_id = int(note_id)

        if note_id < 1:
            return custom_error.BadRequestError().to_dict(), 400

        try:
            deleted_note = sqlalchemy_orm.delete_note_and_related_data_from_db(note_id)
        except sqlalchemy.exc.SQLAlchemyError:
            error_message = util.traceback_custom_error()
            response = custom_error.SQLAlchemyError(error_message).to_dict()
            return response, 500
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500
        else:
            # 존재하지 않은 노트에 대한 처리
            if not deleted_note:
                return custom_error.BadRequestError().to_dict(), 400
            return {'result': True}, 200


    @log.logger_decorator_with_params(log.logger)
    def put(self, note_id):
        if isinstance(note_id, str):
            if not note_id.isdigit():
                return custom_error.BadRequestError().to_dict(), 400
            note_id = int(note_id)

        if note_id < 1:
            return custom_error.BadRequestError().to_dict(), 400

        try:
            new_note_name = request.form['new_note_name']
        except HTTPException:
            error_message = util.traceback_custom_error()
            response = custom_error.HTTPRequestError(error_message).to_dict()
            return response, 400
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 400

        # note_name is not empty
        if not new_note_name:
            return custom_error.BadRequestError().to_dict(), 400

        try:
            sqlalchemy_orm.update_data_to_db(sqlalchemy_orm.Notes, {'note_id' : note_id}, {'note_name' : new_note_name})
        except sqlalchemy.exc.SQLAlchemyError:
            error_message = util.traceback_custom_error()
            response = custom_error.SQLAlchemyError(error_message).to_dict()
            return response, 500
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500
        else:
            return {'result' : True}, 200




class Clause(Resource):
    def __init__(self):
        pass

    @log.logger_decorator_with_params(log.logger)
    def get(self, clause_id):
        if isinstance(clause_id, str):
            if not clause_id.isdigit():
                return custom_error.BadRequestError().to_dict(), 400
            clause_id = int(clause_id)

        if clause_id < 1:
            return custom_error.BadRequestError().to_dict(), 400

        try:
            result = sqlalchemy_orm.get_item_from_db(sqlalchemy_orm.Clauses, {'clause_id' : clause_id})
        except sqlalchemy.exc.SQLAlchemyError:
            error_message = util.traceback_custom_error()
            response = custom_error.SQLAlchemyError(error_message).to_dict()
            return response, 500
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500
        if result:
                return {'clause' : result}, 200
        return {'clause' : []}, 201


    @log.logger_decorator_with_params(log.logger)
    def post(self):
        try:
            note_id = request.form['note_id']
            title = request.form['title']
            contents = request.form['contents']

            if not note_id or not title or not contents:
                return custom_error.BadRequestError().to_dict(), 400

            if isinstance(note_id, str):
                if not note_id.isdigit():
                    return custom_error.BadRequestError().to_dict(), 400
                note_id = int(note_id)

            if note_id < 1:
                return custom_error.BadRequestError().to_dict(), 400

            new_clause_id = sqlalchemy_orm.insert_data_to_db('Clauses', \
                                                             sqlalchemy_orm.Clauses(note_id, \
                                                                                    title, \
                                                                                  contents))
            if not new_clause_id:
                raise custom_error.SQLAlchemyNotInsertError

        except HTTPException:
            error_message = util.traceback_custom_error()
            response = custom_error.HTTPRequestError(error_message).to_dict()
            return response, 400
        except sqlalchemy.exc.SQLAlchemyError:
            error_message = util.traceback_custom_error()
            response = custom_error.SQLAlchemyError(error_message).to_dict()
            return response, 500
        except custom_error.SQLAlchemyNotInsertError:
            return custom_error.SQLAlchemyNotInsertError().to_dict(), 500
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500
        else:
            return {'clause_id' : new_clause_id, 'title' : title, 'contents' : contents}, 200


    @log.logger_decorator_with_params(log.logger)
    def delete(self, clause_id):
        if isinstance(clause_id, str):
            if not clause_id.isdigit():
                return custom_error.BadRequestError().to_dict(), 400
            clause_id = int(clause_id)

        try:
            result = sqlalchemy_orm.delete_data_from_db(sqlalchemy_orm.Clauses, {'clause_id' : clause_id})
            if not result:
                raise custom_error.BadRequestError

        except sqlalchemy.exc.SQLAlchemyError:
            error_message = util.traceback_custom_error()
            response = custom_error.SQLAlchemyError(error_message).to_dict()
            return response, 500
        except custom_error.SQLAlchemyNotInsertError:
            return custom_error.SQLAlchemyNotInsertError().to_dict(), 500
        except custom_error.BadRequestError:
            return custom_error.BadRequestError().to_dict(), 500
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500

        try:
            result = result[0]
            clause_id = getattr(result, 'clause_id')
            return {'clause_id': clause_id}, 200

        except AttributeError:
            error_message = util.traceback_custom_error()
            custom_error.AttributeError(error_message).to_dict()
            return {'clause_id' : None}, 201


    @log.logger_decorator_with_params(log.logger)
    def put(self, clause_id):

        if isinstance(clause_id, str):
            if not clause_id.isdigit():
                return custom_error.BadRequestError().to_dict(), 400
            clause_id = int(clause_id)

        try:
            update_data = {}
            for key, value in request.form.items():
                update_data[key] = value
        except HTTPException:
            error_message = util.traceback_custom_error()
            response = custom_error.HTTPRequestError(error_message).to_dict()
            return response, 400
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500

        try:
            clause = sqlalchemy_orm.update_data_to_db(sqlalchemy_orm.Clauses, {'clause_id' : clause_id}, update_data)
            if not clause:
                raise custom_error.BadRequestError

        except sqlalchemy.exc.SQLAlchemyError:
            error_message = util.traceback_custom_error()
            response = custom_error.SQLAlchemyError(error_message).to_dict()
            return response, 500
        except custom_error.BadRequestError:
            response = custom_error.BadRequestError().to_dict(), 400
            return response, 400
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500
        else:
            return {'clause_id':clause_id, 'clause' : clause}, 200



class ClausePoint(Resource):

    def __init__(self):
        pass

    @log.logger_decorator_with_params(log.logger)
    def get(self, **args):
        try:
            for key, value in request.args.items():
                args[key] = value
        except HTTPException:
            error_message = util.traceback_custom_error()
            response = custom_error.HTTPRequestError(error_message).to_dict()
            return response, 400
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500

        try:
            result = sqlalchemy_orm.get_item_from_db(sqlalchemy_orm.ClausePoints, args)
            if not result:
                raise custom_error.BadRequestError

        except sqlalchemy.exc.SQLAlchemyError:
            error_message = util.traceback_custom_error()
            response = custom_error.SQLAlchemyError(error_message).to_dict()
            return response, 500
        except custom_error.BadRequestError:
            response = custom_error.BadRequestError().to_dict()
            return response, 400
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500
        else:
            return {'note_id': args['note_id'], 'clause_points': result}, 200



    # 포인트 정보 업데이트
    @log.logger_decorator_with_params(log.logger)
    def put(self, clause_id):
        try:
            update_data = {}
            for key, value in request.form.items():
                update_data[key] = value
        except HTTPException:
            error_message = util.traceback_custom_error()
            response = custom_error.HTTPRequestError(error_message).to_dict()
            return response, 400
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500

        try:
            clause_point = sqlalchemy_orm.update_data_to_db(sqlalchemy_orm.ClausePoints, {'clause_id' : clause_id}, update_data)
            if not clause_point:
                raise custom_error.BadRequestError

        except sqlalchemy.exc.SQLAlchemyError:
            error_message = util.traceback_custom_error()
            response = custom_error.SQLAlchemyError(error_message).to_dict()
            return response, 500
        except custom_error.BadRequestError:
            response = custom_error.BadRequestError().to_dict()
            return response, 400
        except:
            error_message = util.traceback_custom_error()
            response = custom_error.UnExpectedError(error_message).to_dict()
            return response, 500
        else:
            return {'clause_id': clause_id, 'clause_point' : clause_point}, 200




api.add_resource(Note, '/api/notes','/api/notes/<note_id>')
api.add_resource(Clause, '/api/clauses', '/api/clauses/<clause_id>')
api.add_resource(ClausePoint, '/api/notes/<note_id>/clausePoints', '/api/clausePoints/<clause_id>')
