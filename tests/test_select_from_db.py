import logging
import os
import unittest

from studi import app
from studi import sqlite_db
from studi import upload
from studi.sqlite_db import Notes, ClausePoints, Clauses


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
    """
    if you want to skip some function, use it.
    @unittest.skip("skipping")
    """

    def setUp(self):
        self.app = app.test_client()
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

        # create new testing db & insert dummy data
        if os.path.exists("../studi/db/test_studi.db"):
            sqlite_db.drop_db(False)
        self.db = sqlite_db.create_db(False)
        upload.insert_csv_to_db(False)


    def test_select_all_notes(self):
        with app.app_context():
            try:
                result = None
                result = sqlite_db.get_all_data_from_db(Notes)
            except:
                logger.debug('Cannot select Notes')
            finally:
                self.assertIsNotNone(result)
                self.assertIsInstance(result, list)


    def test_select_clauses_by_clause_id(self):
        with app.app_context():
            try:
                result = sqlite_db.get_item_from_db(Clauses, {'clause_id' : 1})
            except Exception as exc:
                logger.debug("Cannot select Clauses, clause_id : 1, exc : {0} ".format(exc))
            finally:
                self.assertIsNotNone(result)
                self.assertNotEqual(len(result), 0)
                self.assertEqual(result[0]['clause_id'], 1)


    def test_select_clauses_by_note_id(self):
        with app.app_context():
            try:
                result = sqlite_db.get_item_from_db(Clauses, {'note_id':1})
            except:
                logger.debug("Cannot select Clauses, note_id : 1, note_id : 1")
            finally:
                self.assertIsNotNone(result)
                self.assertIsInstance(result, list)
                self.assertNotEqual(len(result), 0)
                self.assertEqual(result[0]['note_id'], 1)


    def test_select_clausePoints_by_note_id(self):
        with app.app_context():
            try:
                result = sqlite_db.get_item_from_db(ClausePoints, {'note_id':1, 'clause_id':1})
            except:
                logger.debug("Cannot select ClausePoints, note_id : 1, caluse_id : 1")
            finally:
                self.assertIsNotNone(result)
                self.assertIsInstance(result, list)
                self.assertNotEqual(len(result), 0)
                self.assertEqual(result[0]['note_id'], 1)
                self.assertEqual(result[0]['clause_id'], 1)


if __name__ == '__main__':
    unittest.main()