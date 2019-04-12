
from flask_restful import Api, Resource
from studi import sqlite_db
from studi import app
from flask import request
from studi import upload
import csv

api = Api(app)


class Notes(Resource):
    def __init__(self):
        pass

    def get(self):
        try:
            result = sqlite_db.get_all_data_from_db(sqlite_db.Note)
        except Exception as exc:
            app.logger.warn("Exception raised during 'GET date from Notes; {0}".format(str(exc)))
            return {'notes' : None}, 500
        else:
            if result:
                notes = []
                for item in result:
                    note = dict()
                    for name in sqlite_db.Note.column:
                        note[name] = getattr(item, name)
                    notes.append(note)
                return {'notes' : notes}, 200
            else:
                return {'notes' : None}, 201


    def post(self):
        try:
            file = request.files['studi_material']
            file_name = file.filename

            # Cross-site scripting (XSS)
            if file_name[-3:] != "csv":
                app.logger.warn(
                    "Exception raised during upload new file file name is : {0}".format(file_name))
                return {'result' : False, \
                        'description' : "file's extenstion is not .csv. You should upload csv file. \
                        Uploaded file name is : {0}".format(file_name)}, 400

            request_file = request.files['studi_material']
            csvfile = request_file.read().decode("utf-8").splitlines()
            note = csv.DictReader(csvfile)
            if upload.save_csv_contents_to_db(file_name[:-3], note, True):
                return {'result': True}, 200
            else:
                return {'result': False}, 400
        except Exception as exc:
            app.logger.warn("Exception raised during POST note to Notes; {0}".format(str(exc)))
            return {'result' : False}, 500


    def delete(self, note_id):
        try:
            sqlite_db.delete_note_and_related_data_from_db(int(note_id))
        except Exception as exc:
            app.logger.warn("Exception raised during Delete note from Notes; {0}".format(str(exc)))
            return {'result' : False}, 500
        else:
            # Todo ADD Verification Code
            return {'result': True}, 200


    def put(self, note_id):
        new_note_name = request.form['note_name']
        pass



class Clause(Resource):
    def __init__(self):
        pass

    def post(self, clause_id):
        try:
            result = sqlite_db.get_item_from_db(sqlite_db.Clauses, {'clause_id' : clause_id})
        except Exception as exc:
            app.logger.warn(
                "Exception raised during get data from clause ".format( clause_id, str(exc))
            )
            return { 'clause_id': clause_id, 'title': None, 'contents': None }, 500
        if result:
            try:
                result = result[0]
                title = result.title
                contents = result.contents
                return { 'clause_id': clause_id, 'title': title, 'contents': contents }, 200
            except Exception as exc:
                app.logger.warn(
                    "Exception raised during access to query row item {0}: {1}".format(
                        result, str(exc)
                    )
                )
                return { 'clause_id': clause_id, 'title': None, 'contents': None }, 500
        else:
            return { 'clause_id': clause_id, 'title': None, 'contents': None }, 201


class ClausePoint(Resource):

    def __init__(self):
        pass

    def post(self, note_id):
        #todo imp, und 세부 조건 추가로 받아서 처리
        try:
            result = sqlite_db.get_item_from_db(sqlite_db.ClausePoints, {'note_id' : note_id})
        except Exception as exc:
            app.logger.warn(
                "Exception raised during 'SELECT * FROM ClausePoints WHERE note_id={0}' query: {1}".format(
                    note_id, str(exc)
                )
            )
            return { 'note_id': note_id, 'clause_points': None }, 500
        if result:
            clause_points = []
            for item in result:
                point = dict()
                for key in item.keys():
                    if key != 'note_id':
                        point[key] = item[key]
                clause_points.append(point)
            return { 'note_id': note_id, 'clause_points': clause_points }, 200
        else:
            return { 'note_id': note_id, 'clause_points': None }, 201


    # 포인트 정보 업데이트
    def put(self, clause_id):
        pass
        """
        data = request.form['data']
        return {'result' : True, 'clause_id': clause_id, 'data' : data}, 200

        try:
            sqlite_db.update_data_to_db(sqlite_db.ClausePoints, clause_id, {'imp' : imp, 'und' : und})
        except Exception as exc:
            app.logger.warn("Exception raised during 'Update point data to ClausePoints.\
            clause_id : {0}, imp : {1}, und : {2}".format(clause_id, imp, und, str(exc)))
            return {'result': False}, 500
        else:
            #todo update 결과에 대한 검증 추가
            return {'result': True}, 200
        """


api.add_resource(Notes, '/notes', '/', '/note/<note_id>')
api.add_resource(Clause, '/clause', '/clause/<clause_id>')
api.add_resource(ClausePoint, '/clausePoint', '/clausePoint/<note_id>', '/clausePoint/<clause_id>')
