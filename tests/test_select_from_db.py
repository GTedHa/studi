import logging
import os
import unittest

from studi import app
from studi import sqlite_db
from studi import upload
from studi.sqlite_db import Note, ClausePoints, Clauses


def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(app.config['LOG_DIR'], test_name + '.log'))
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger

test_name = "test_select_from_db"
logger = gen_logger(test_name)

class TestSelectDB(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

        # create new testing db & insert dummy data
        if os.path.exists("../studi/db/test_studi.db"):
            sqlite_db.drop_db(production=False)
        self.db = sqlite_db.create_db(production=False)
        upload.insert_csv_to_db(False)


    def test_select_all_notes(self):
        with app.app_context():
            try:
                result = sqlite_db.get_all_data_from_db(Note)
            except:
                logger.debug('Cannot select Notes')
            else:
                self.assertIsNotNone(result)
                if result:
                    notes = []
                    for item in result:
                        note = dict()
                        for key in item.column:
                            note[key] = getattr(item, key)
                        notes.append(note)


    def test_select_clauses_by_note_id(self):
        with app.app_context():
            try:
                result = sqlite_db.get_item_from_db(Clauses, {'note_id':1})
            except:
                logger.debug("Cannot select Clauses by note_id, note_id : 1")
            else:
                self.assertIsNotNone(result)
                if result:
                    clauses = []
                    for item in result:
                        clause = dict()
                        for key in item.column:
                            clause[key] = getattr(item, key)
                            self.assertIsNotNone(clause[key])
                        clauses.append(clause)


    def test_select_clausePoints_by_note_id(self):
        with app.app_context():
            try:
                result = sqlite_db.get_item_from_db(ClausePoints, {'note_id':1, 'clause_id':1})
            except:
                logger.debug("Cannot select ClausePoints_by_note_id, note_id : 1, caluse_id : 1")
            else:
                self.assertIsNotNone(result)
                if result:
                    clausePoints = []
                    for item in result:
                        clausePoint = dict()
                        for key in item.column:
                            clausePoint[key] = getattr(item, key)
                            self.assertIsNotNone(clausePoint[key])
                        clausePoints.append(clausePoint)

if __name__ == '__main__':
    unittest.main()