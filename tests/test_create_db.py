import logging
import os
import unittest
from flask_sqlalchemy import SQLAlchemy

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
        self.app = studi.app.test_client()


    def test_create_db(self):
        with studi.app.app_context():
            try:
                # init ../db/test_studi.db
                db = sqlite_db.create_db(production=False)
                logger.info("create db success!")
            except:
                logger.debug("Cannot create db..")
            else:
                table_names = db.engine.table_names()
                self.assertIn('note', table_names)
                self.assertIn('clauses', table_names)
                self.assertIn('clause_points', table_names)

    def test_delete_db(self):
        with studi.app.app_context():
            try:
                sqlite_db.drop_db(production=False)
                logger.info("Delete db success!")
            except:
                logger.debug('Cannot delete db..')


if __name__ == "__main__":
    unittest.main()