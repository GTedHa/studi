import logging
import os
import sqlalchemy
import unittest

from studi import app
from studi import sqlalchemy_orm, upload, util, custom_error
from studi.sqlalchemy_orm import Notes, Clauses, ClausePoints


def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(app.config['TEST_LOG_DIR'], test_name + '.log'))
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger

test_name = "test_delete"
logger = gen_logger(test_name)

class TestDeleteDB(unittest.TestCase):
    """
    if you want to skip some function, use it.
    @unittest.skip("skipping")
    """
    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

        #create new tesint DB & insert dummy data
        if os.path.exists("../studi/db/test_studi.db"):
            sqlalchemy_orm.drop_db(False)
        sqlalchemy_orm.create_db(False)
        upload.insert_csv_to_db(False)  # note_id : 1
        upload.insert_csv_to_db(False)  # note_id : 2
        upload.insert_csv_to_db(False)  # note_id : 3


    # Delete one Note (with related clause, clausePoints Data)
    # @unittest.skip("skipping")
    def test_delete_one_note(self):
        with app.app_context():
            try:
                sqlalchemy_orm.delete_note_and_related_data_from_db(3)
                # Check if result is empty
                note_result = sqlalchemy_orm.get_item_from_db(Notes, {'note_id' : 3})
                clauses_result = sqlalchemy_orm.get_item_from_db(Clauses, {'note_id' : 3})
                clausePoints_result = sqlalchemy_orm.get_item_from_db(ClausePoints, {'note_id' : 3})
                self.assertEqual(note_result, [])
                self.assertEqual(clauses_result, [])
                self.assertEqual(clausePoints_result, [])

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


    # Delete multiple Note (with related clause, clausePoints Data)
    # @unittest.skip("skipping")
    def test_delete_multiple_note(self):
        with app.app_context():
            try:
                sqlalchemy_orm.delete_data_from_db(Notes, {'note_id' : [1, 2]})
                # Check if result is empty
                note_result = sqlalchemy_orm.get_item_from_db(Notes, {'note_id' : [1, 2]})
                self.assertEqual(note_result, [])

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


    # Delete Clause (with related clausePoints)
    # @unittest.skip("skipping")
    def test_delete_clause(self):
        with app.app_context():
            try:
                sqlalchemy_orm.delete_data_from_db(Clauses, {'clause_id' : 11})
                clause_result = sqlalchemy_orm.get_item_from_db(Clauses, {'clause_id' : 11})
                clause_point_result = sqlalchemy_orm.get_item_from_db(ClausePoints, {'clause_id' : 11})

                # Check if result is empty
                self.assertEqual(clause_result,[])
                self.assertEqual(clause_point_result, [])

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






