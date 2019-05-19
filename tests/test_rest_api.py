# coding=utf-8

import logging
import os
import unittest
import json
import sqlalchemy


from studi import app
from studi import upload, util, custom_error

from studi import sqlalchemy_orm


def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(app.config['TEST_LOG_DIR'], test_name + '.log'))
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger

test_name = "test_rest_api"
logger = gen_logger(test_name)

class TestRestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

        # create new testing db & insert dummy data
        if os.path.exists("../studi/db/test_studi.db"):
            sqlalchemy_orm.drop_db(False)
        self.db = sqlalchemy_orm.create_db(False)
        upload.insert_csv_to_db(False) # note_id : 1
        upload.insert_csv_to_db(False) # note_id : 2
        upload.insert_csv_to_db(False) # note_id : 3

    # @unittest.skip("skipping")
    def test_get_notes(self):
        with app.app_context():
            try:
                resp = self.app.get('/api/notes')
                data = json.loads(resp.data)
                self.assertIsInstance(data['notes'], list)
                self.assertNotEqual(len(data['notes']), 0)
                self.assertEqual(resp.status_code, 200)

            except sqlalchemy.exc.SQLAlchemyError:
                error_message = util.traceback_custom_error()
                error = custom_error.SQLAlchemyError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except AssertionError:
                error_message = util.traceback_custom_error()
                error = custom_error.AssertionError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except:
                error_message = util.traceback_custom_error()
                error = custom_error.UnExpectedError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise


    # @unittest.skip("skipping")
    def test_post_note(self):
        with app.app_context():
            try:
                data = {
                    'studi_material': open('../studi/uploads/studi_test_file.csv', 'rb')
                }
                resp = self.app.post('/api/notes', data=data, content_type='multipart/form-data')
                data = json.loads(resp.data)
                self.assertEqual(data['result'], True)
                self.assertEqual(resp.status_code, 200)

            except sqlalchemy.exc.SQLAlchemyError:
                error_message = util.traceback_custom_error()
                error = custom_error.SQLAlchemyError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except AssertionError:
                error_message = util.traceback_custom_error()
                error = custom_error.AssertionError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except:
                error_message = util.traceback_custom_error()
                error = custom_error.UnExpectedError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise

    # @unittest.skip("skipping")
    def test_delete_note(self):
        with app.app_context():
            try:
                resp = self.app.delete('/api/notes/1')
                data = json.loads(resp.data)
                self.assertEqual(data['result'], True)
                self.assertEqual(resp.status_code, 200)

            except sqlalchemy.exc.SQLAlchemyError:
                error_message = util.traceback_custom_error()
                error = custom_error.SQLAlchemyError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except AssertionError:
                error_message = util.traceback_custom_error()
                error = custom_error.AssertionError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except:
                error_message = util.traceback_custom_error()
                error = custom_error.UnExpectedError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise

    # @unittest.skip("skipping")
    def test_put_note(self):
        with app.app_context():
            try:
                data = {
                    'new_note_name' : 'new_note_name'
                }
                resp = self.app.put('/api/notes/1', data=data, content_type='multipart/form-data')
                data = json.loads(resp.data)
                self.assertEqual(data['result'], True)
                self.assertEqual(resp.status_code, 200)

            except sqlalchemy.exc.SQLAlchemyError:
                error_message = util.traceback_custom_error()
                error = custom_error.SQLAlchemyError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except AssertionError:
                error_message = util.traceback_custom_error()
                error = custom_error.AssertionError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except:
                error_message = util.traceback_custom_error()
                error = custom_error.UnExpectedError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise

    # @unittest.skip("skipping")
    def test_get_clause(self):
        with app.app_context():
            try:
                resp = self.app.get('/api/clauses/1')
                data = json.loads(resp.data)
                self.assertIsNotNone(data['clause'])
                self.assertEqual(resp.status_code, 200)

            except sqlalchemy.exc.SQLAlchemyError:
                error_message = util.traceback_custom_error()
                error = custom_error.SQLAlchemyError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except AssertionError:
                error_message = util.traceback_custom_error()
                error = custom_error.AssertionError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except:
                error_message = util.traceback_custom_error()
                error = custom_error.UnExpectedError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise

    # @unittest.skip("skipping")
    def test_post_clause(self):
        with app.app_context():
            try:
                data = {
                    'note_id' : 1,
                    'title' : '특별한 날',
                    'contents': '특별한 날에 대한 설명'
                }
                resp = self.app.post('/api/clauses', data=data, content_type='multipart/form-data')
                data = json.loads(resp.data)
                self.assertIsNotNone(data['clause_id'])
                self.assertEqual(resp.status_code, 200)

            except sqlalchemy.exc.SQLAlchemyError:
                error_message = util.traceback_custom_error()
                error = custom_error.SQLAlchemyError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except AssertionError:
                error_message = util.traceback_custom_error()
                error = custom_error.AssertionError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except:
                error_message = util.traceback_custom_error()
                error = custom_error.UnExpectedError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise

    # @unittest.skip("skipping")
    def test_delete_clause(self):
        with app.app_context():
            try:
                resp = self.app.delete('/api/clauses/2')
                data = json.loads(resp.data)
                self.assertEqual(resp.status_code, 200)

            except sqlalchemy.exc.SQLAlchemyError:
                error_message = util.traceback_custom_error()
                error = custom_error.SQLAlchemyError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except AssertionError:
                error_message = util.traceback_custom_error()
                error = custom_error.AssertionError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except:
                error_message = util.traceback_custom_error()
                error = custom_error.UnExpectedError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise

    # @unittest.skip("skipping")
    def test_put_clause(self):
        with app.app_context():
            try:
                data = {
                    'title' : '변경된 제목',
                    'contents' : '변경된 내용'
                }
                resp = self.app.put('/api/clauses/2', data=data, content_type='multipart/form-data')
                data = json.loads(resp.data)
                self.assertIsNotNone(data['clause'])
                self.assertNotEqual(len(data['clause']), 0)
                self.assertEqual(resp.status_code, 200)

            except sqlalchemy.exc.SQLAlchemyError:
                error_message = util.traceback_custom_error()
                error = custom_error.SQLAlchemyError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except AssertionError:
                error_message = util.traceback_custom_error()
                error = custom_error.AssertionError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except:
                error_message = util.traceback_custom_error()
                error = custom_error.UnExpectedError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise


    # @unittest.skip("skipping")
    def test_get_clausepoints(self):
        with app.app_context():
            try:
                # update for testing
                sqlalchemy_orm.update_data_to_db(sqlalchemy_orm.ClausePoints, {'clause_id': 7}, {'imp': 0, 'und': 1})
                sqlalchemy_orm.update_data_to_db(sqlalchemy_orm.ClausePoints, {'clause_id': 6}, {'imp': 1, 'und': 1})
                sqlalchemy_orm.update_data_to_db(sqlalchemy_orm.ClausePoints, {'clause_id': 5}, {'imp': 1, 'und': 1})

                params = {
                    'imp' : 1,
                    'und' : 1
                }
                resp = self.app.get('/api/notes/2/clausePoints', query_string=params)
                data = json.loads(resp.data)
                self.assertEqual(resp.status_code, 200)
                self.assertIsNotNone(data['clause_points'])
                self.assertNotEqual(len(data['clause_points']), 0)

            except sqlalchemy.exc.SQLAlchemyError:
                error_message = util.traceback_custom_error()
                error = custom_error.SQLAlchemyError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except AssertionError:
                error_message = util.traceback_custom_error()
                error = custom_error.AssertionError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except:
                error_message = util.traceback_custom_error()
                error = custom_error.UnExpectedError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise


    # @unittest.skip("skipping")
    def test_put_clausepoint(self):
        with app.app_context():
            try:
                data = {
                    'imp' : 1,
                    'und' : 1
                }
                resp = self.app.put('/api/clausePoints/1', data = data, content_type='multipart/form-data')
                data = json.loads(resp.data)
                self.assertEqual(resp.status_code, 200)
                self.assertIsNotNone(data['clause_point'])
                self.assertNotEqual(len(data['clause_point']), 0)

            except sqlalchemy.exc.SQLAlchemyError:
                error_message = util.traceback_custom_error()
                error = custom_error.SQLAlchemyError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except AssertionError:
                error_message = util.traceback_custom_error()
                error = custom_error.AssertionError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise
            except:
                error_message = util.traceback_custom_error()
                error = custom_error.UnExpectedError(error_message)
                error.set_logger(logger)
                error.to_dict()
                raise


if __name__ == "__main__":
    unittest.main()


