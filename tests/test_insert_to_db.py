import logging
import os
import unittest

import studi
from studi import sqlite_db
from flask_sqlalchemy import SQLAlchemy


def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(studi.app.config['LOG_DIR'], test_name + '.log'))
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger

test_name = "test_insert_db"
logger = gen_logger(test_name)
#
# sqlite_db.create_db(production=False)
# print('11')

class TestInsertDB(unittest.TestCase):


    def setUp(self):
        studi.app.testing = True
        self.app = studi.app.test_client()
        # create new testing db
        if os.path.exists("../studi/db/test_studi.db"):
            sqlite_db.drop_db(production=False)
        self.db = sqlite_db.create_db(production=False)


    def test_insert_note_db(self):
        with studi.app.app_context():
            try:
                Note = sqlite_db.Note
                note_id  = sqlite_db.insert_data_to_db('Note', Note('test_title_1'))
                logger.info("Insert data table(Note) success! id : {0}".format(note_id))
            except:
                logger.debug('Cannot insert data to db(Note)..')
            else:
                self.assertIsNotNone(note_id)


    def test_insert_clause_db(self):
        with studi.app.app_context():
            try:
                Clauses = sqlite_db.Clauses
                clauses_id = sqlite_db.insert_data_to_db('Clauses', Clauses(1, "test_clause_1", "test_content_1"))
                logger.info("Insert data to table(Clauses) success! cluases_id : {0}".format(clauses_id))
            except:
                logger.debug("Cannot insert to db(Clauses)")
            else:
                self.assertIsNotNone(clauses_id)


    def test_insert_clausePoints_db(self):
        with studi.app.app_context():
            try:
                clausePoints = sqlite_db.ClausePoints
                # column = ['clause_id', 'note_id', 'imp', 'und']
                clausepoints_id = sqlite_db.insert_data_to_db("ClausePoints", clausePoints(1, 1))
                logger.info("Insert data to table(ClausePoints success! clausepoints_id : {0}".format(clausepoints_id))
            except:
                logger.debug("Cannot insert to db(CluasePoints)")
            else:
                self.assertIsNotNone(clausepoints_id)


    def test_insert_csv_to_db(self):
        pass

    def tearDown(self):
        sqlite_db.drop_db(production=False)
        studi.app.testing = False



if __name__ == "__main__":
    unittest.main()





