import logging
import os
import unittest

from studi import app
from studi import sqlite_db
from studi import upload
from studi.sqlite_db import Note, Clauses, ClausePoints

def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(app.config['LOG_DIR'], test_name + '.log'))
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger

test_name = "test_delete_from_db"
logger = gen_logger(test_name)

class TestDeleteDB(unittest.TestCase):
    """
    if you want to skip some function, use it.
    @unittest.skip("skipping")
    """


    def setUp(self):
        self.app = app.test_client()
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

        #create new tesint DB & insert dummy data
        if os.path.exists("../studi/db/test_studi.db"):
            sqlite_db.drop_db(False)
        sqlite_db.create_db(False)
        upload.insert_csv_to_db(False)  # note_id : 1
        upload.insert_csv_to_db(False)  # note_id : 2
        upload.insert_csv_to_db(False)  # note_id : 3


    # Delete one Note (with related clause, clausePoints Data)
    # @unittest.skip("skipping")
    def test_delete_one_note(self):
        with app.app_context():
            try:
                sqlite_db.delete_note_and_related_data_from_db(3)
            except Exception as exc:
                logger.debug('Cannot delete note and related data from other tables, because {0}'.format(exc))
            else:
                # Check if result is empty
                note_result = sqlite_db.get_item_from_db(Note, {'note_id' : 3})
                clauses_result = sqlite_db.get_item_from_db(Clauses, {'note_id' : 3})
                clausePoints_result = sqlite_db.get_item_from_db(ClausePoints, {'note_id' : 3})
                self.assertCountEqual(note_result, [])
                self.assertCountEqual(clauses_result, [])
                self.assertCountEqual(clausePoints_result, [])



    # Delete multiple Note (with related clause, clausePoints Data)
    @unittest.skip("skipping")
    def test_delete_multiple_note(self):
        with app.app_context():
            try:
                sqlite_db.delete_data_from_db(Note, {'note_id' : [1,2]})
            except Exception as exc:
                logger.debug("Cannot delete multiple notes data, because : {0}".format(exc))
            else:
                # Check if result is empty
                result = sqlite_db.get_item_from_db(Note, {'note_id' : [1,2]})
                self.assertCountEqual(result, [])


    # Delete Clause (with related clausePoints)
    @unittest.skip("skipping")
    def test_delete_clause(self):
        with app.app_context():
            try:
                sqlite_db.delete_data_from_db(Clauses, {'clause_id' : 11})
            except Exception as exc:
                logger.debug("Cannot delete clause and related points data, baluse : {0}".format(exc))
            else:
                clause_result = sqlite_db.get_item_from_db(Clauses, {'clause_id' : 11})
                clause_point_result = sqlite_db.get_item_from_db(ClausePoints, {'clause_id' : 11})

                # Check if result is empty
                self.assertCountEqual(clause_result,[])
                self.assertCountEqual(clause_point_result, [])



if __name__ == "__main__":
    unittest.main()






