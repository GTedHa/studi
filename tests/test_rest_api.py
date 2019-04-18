# coding=utf-8

import logging
import os
import unittest
from studi import app
from studi import upload
import json
from flask import jsonify

import studi
from studi import sqlite_db


def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(studi.app.config['LOG_DIR'], test_name + '.log'))
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger

test_name = "test_rest_api"
logger = gen_logger(test_name)

class TestRestAPI(unittest.TestCase):

    def setUp(self):
        studi.app.testing = True
        self.app = studi.app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'


        # create new testing db & insert dummy data
        if os.path.exists("../studi/db/test_studi.db"):
            sqlite_db.drop_db(False)
        self.db = sqlite_db.create_db(False)
        upload.insert_csv_to_db(False) # note_id : 1
        upload.insert_csv_to_db(False) # note_id : 2
        upload.insert_csv_to_db(False) # note_id : 3

    # @unittest.skip("skipping")
    def test_get_notes(self):
        with studi.app.app_context():
            try:
                resp = self.app.get('/notes')
            except Exception as exc:
                print('GET Notes, Error : {0}'.format(exc))
            else:
                data = json.loads(resp.data)
                self.assertIsInstance(data['notes'], list)
                self.assertNotEqual(len(data['notes']), 0)
                self.assertEqual(resp.status_code, 200)

    # @unittest.skip("skipping")
    def test_get_note(self):
        with studi.app.app_context():
            try:
                resp = self.app.get('/note/2')
            except Exception as exc:
                print('GET note, Error : {0}'.format(exc))
            else:
                data = json.loads(resp.data)
                self.assertIsInstance(data['notes'], list)
                self.assertEqual(resp.status_code, 200)

    # @unittest.skip("skipping")
    def test_post_note(self):
        with studi.app.app_context():
            try:
                data = {
                    'studi_material': open('../studi/uploads/studi_test_file.csv', 'rb')
                }
                resp = self.app.post('/note', data=data, content_type='multipart/form-data')
            except Exception as exc:
                print('POST Note, Error : {0}'.format(exc))
            else:
                data = json.loads(resp.data)
                self.assertEqual(data['result'], True)
                self.assertEqual(resp.status_code, 200)

    # @unittest.skip("skipping")
    def test_delete_note(self):
        with studi.app.app_context():
            try:
                resp = self.app.delete('note/1')
            except Exception as exc:
                print('DELETE Note, Error : {0}'.format(exc))
            else:
                data = json.loads(resp.data)
                self.assertEqual(data['result'], True)
                self.assertEqual(resp.status_code, 200)

    # @unittest.skip("skipping")
    def test_put_note(self):
        with studi.app.app_context():
            try:
                data = {
                    'new_note_name' : 'new_note_name'
                }
                resp = self.app.put('/note/1', data=data, content_type='multipart/form-data')
            except Exception as exc:
                print('PUT note name, Error : {0}'.format(exc))
            else:
                data = json.loads(resp.data)
                self.assertEqual(data['result'], True)
                self.assertEqual(resp.status_code, 200)

    # @unittest.skip("skipping")
    def test_get_clause(self):
        with studi.app.app_context():
            try:
                resp = self.app.get('/clause/1')
            except Exception as exc:
                print('GET clause, Error : {0}'.format(exc))
            else:
                data = json.loads(resp.data)
                self.assertIsNotNone(data['clause'])
                self.assertEqual(resp.status_code, 200)

    # @unittest.skip("skipping")
    def test_post_clause(self):
        with studi.app.app_context():
            try:
                data = {
                    'note_id' : 1,
                    'title' : '특별한 날',
                    'contents': '특별한 날에 대한 설명'
                }
                resp = self.app.post('/clause', data=data, content_type='multipart/form-data')
            except Exception as exc:
                print('POST new clause, Error : {0}'.format(exc))
            else:
                data = json.loads(resp.data)
                self.assertIsNotNone(data['clause_id'])
                self.assertEqual(resp.status_code, 200)

    # @unittest.skip("skipping")
    def test_delete_clause(self):
        with studi.app.app_context():
            try:
                resp = self.app.delete('/clause/2')
            except Exception as exc:
                print('DELETE clause, Error : {0}'.format(exc))
            else:
                data = json.loads(resp.data)
                self.assertEqual(resp.status_code, 200)

    # @unittest.skip("skipping")
    def test_put_clause(self):
        with studi.app.app_context():
            try:
                data = {
                    'title' : '변경된 제목',
                    'contents' : '변경된 내용'
                }
                resp = self.app.put('/clause/2', data=data, content_type='multipart/form-data')
            except Exception as exc:
                print('PUT cluase title, contents, Error : {0}'.format(exc))
            else:
                data = json.loads(resp.data)
                self.assertIsNotNone(data['clause'])
                self.assertNotEqual(len(data['clause']), 0)
                self.assertEqual(resp.status_code, 200)


    # @unittest.skip("skipping")
    def test_get_clausepoints(self):
        with studi.app.app_context():
            try:
                # update for testing
                sqlite_db.update_data_to_db(sqlite_db.ClausePoints, {'clause_id': 7}, {'imp': 0, 'und': 1})
                sqlite_db.update_data_to_db(sqlite_db.ClausePoints, {'clause_id': 6}, {'imp': 1, 'und': 1})
                sqlite_db.update_data_to_db(sqlite_db.ClausePoints, {'clause_id': 5}, {'imp': 1, 'und': 1})

                params = {
                    'imp' : 1,
                    'und' : 1
                }
                resp = self.app.get('note/2/clausePoint', query_string=params)
            except Exception as exc:
                print('GET clausepoint, Error : {0}'.format(exc))
            else:
                data = json.loads(resp.data)
                self.assertEqual(resp.status_code, 200)
                self.assertIsNotNone(data['clause_points'])
                self.assertNotEqual(len(data['clause_points']), 0)

    # @unittest.skip("skipping")
    def test_put_clausepoint(self):
        with studi.app.app_context():
            try:
                data = {
                    'imp' : 1,
                    'und' : 1
                }
                resp = self.app.put('/clausePoint/1', data = data, content_type='multipart/form-data' )
            except Exception as exc:
                print('put clausepoint, Error : {0}'.format(exc))
            else:
                data = json.loads(resp.data)
                self.assertEqual(resp.status_code, 200)
                self.assertIsNotNone(data['clause_point'])
                self.assertNotEqual(len(data['clause_point']), 0)


if __name__ == "__main__":
    unittest.main()


