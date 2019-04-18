import logging
import os
import unittest

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

test_name = "test_create_db"
logger = gen_logger(test_name)


# Testing that create DB by using flask_sqlalchemy(ORM)
class TestCreateDB(unittest.TestCase):

    def setUp(self):
        studi.app.testing = True
        studi.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

        # delete db
        if os.path.exists("../studi/db/test_studi.db"):
            sqlite_db.drop_db(False)
            self.app = studi.app.test_client()


    def test_create_db(self):
        with studi.app.app_context():
            try:
                db = sqlite_db.create_db(False)
            except Exception as exc:
                logger.debug("Cannot create db, Error : {0}".format(exc))
            finally:
                table_names = db.engine.table_names()
                self.assertIn('notes', table_names)
                self.assertIn('clauses', table_names)
                self.assertIn('clause_points', table_names)

    def test_delete_db(self):
        with studi.app.app_context():
            try:
                db = sqlite_db.drop_db(False)
            except Exception as exc:
                logger.debug('Cannot delete db, Error : {1}'.format(exc))
            finally:
                table_names = db.engine.table_names()
                self.assertEqual(table_names, [])
                self.assertEqual(len(table_names), 0)


    def tearDown(self):
        studi.app.testing = False

if __name__ == "__main__":
    unittest.main()