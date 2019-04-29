import logging
import os
import unittest

import studi
from studi import sqlalchemy
from studi import upload


def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(studi.app.config['LOG_DIR'], test_name + '.log'))
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger

test_name = "test_insert"
logger = gen_logger(test_name)

class TestInsertDB(unittest.TestCase):
    """
    if you want to skip some function, use it.
    @unittest.skip("skipping")
    """

    def setUp(self):
        studi.app.testing = True
        self.app = studi.app.test_client()
        # create new testing db
        if os.path.exists("../studi/db/test_studi.db"):
            sqlalchemy.drop_db(False)
        self.db = sqlalchemy.create_db(False)


    def test_insert_note_db(self):
        with studi.app.app_context():
            try:
                Notes = sqlalchemy.Notes
                note_id  = sqlalchemy.insert_data_to_db('Notes', Notes('test_title_1'))
            except Exception as exc:
                logger.debug('Cannot insert data to db(Notes), Error : {0}'.format(exc))
            finally:
                self.assertIsNotNone(note_id)


    def test_insert_clause_db(self):
        with studi.app.app_context():
            try:
                Clauses = sqlalchemy.Clauses
                clauses_id = sqlalchemy.insert_data_to_db('Clauses', Clauses(1, "test_clause_1", "test_content_1"))
            except Exception as exc:
                logger.debug("Cannot insert to db(Clauses), Error : {0}".format(exc))
            finally:
                self.assertIsNotNone(clauses_id)


    def test_insert_clausePoints_db(self):
        with studi.app.app_context():
            try:
                clausePoints = sqlalchemy.ClausePoints
                # column = ['clause_id', 'note_id', 'imp', 'und']
                clausepoints_id = sqlalchemy.insert_data_to_db("ClausePoints", clausePoints(1, 1))
            except Exception as exc:
                logger.debug("Cannot insert to db(CluasePoints), Error: {0}".format(exc))
            finally:
                self.assertIsNotNone(clausepoints_id)


    def test_insert_csv_to_db(self):
        with studi.app.app_context():
            if os.path.exists('../studi/uploads/studi_test_file.csv'):
                try:
                    note_id = upload.insert_csv_to_db()
                except Exception as exc:
                    logger.debug("Cannot read csv file Even though csv file exists, Error : {0}".format(exc))
                finally:
                    self.assertIsNotNone(note_id)
            else:
                logger.debug("There is not csv file")


    def tearDown(self):
        studi.app.testing = False


if __name__ == "__main__":
    unittest.main()





