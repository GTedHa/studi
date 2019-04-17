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

    def test_get_notes(self):
        with studi.app.app_context():
            try:
                resp = self.app.get('/notes')
            except Exception as exc:
                print('GET Notes, Error : {0}'.format(exc))
            else:
                self.assertEqual(resp.status_code, 200)

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


    def test_put_note(self):
        pass
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


if __name__ == "__main__":
    unittest.main()


