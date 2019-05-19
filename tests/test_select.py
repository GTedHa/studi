import logging
import os
import sqlalchemy
import unittest

from studi import app
from studi import sqlalchemy_orm, upload, util, custom_error
from studi.sqlalchemy_orm import Notes, ClausePoints, Clauses


def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(app.config['TEST_LOG_DIR'], test_name + '.log'))
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger


test_name = "test_select"
logger = gen_logger(test_name)

class TestSelectDB(unittest.TestCase):
    """
    if you want to skip some function, use it.
    @unittest.skip("skipping")
    """

    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

        # create new testing db & insert dummy data
        if os.path.exists("../studi/db/test_studi.db"):
            sqlalchemy_orm.drop_db(False)
        self.db = sqlalchemy_orm.create_db(False)
        upload.insert_csv_to_db(False)


    def test_select_all_notes(self):
        with app.app_context():
            try:
                result = None
                result = sqlalchemy_orm.get_all_data_from_db(Notes)
                self.assertIsNotNone(result)
                self.assertIsInstance(result, list)

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


    def test_select_clauses_by_clause_id(self):
        with app.app_context():
            try:
                result = sqlalchemy_orm.get_item_from_db(Clauses, {'clause_id' : 1})
                self.assertIsNotNone(result)
                self.assertNotEqual(len(result), 0)
                self.assertEqual(result[0]['clause_id'], 1)

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


    def test_select_clauses_by_note_id(self):
        with app.app_context():
            try:
                result = sqlalchemy_orm.get_item_from_db(Clauses, {'note_id':1})
                self.assertIsNotNone(result)
                self.assertIsInstance(result, list)
                self.assertNotEqual(len(result), 0)
                self.assertEqual(result[0]['note_id'], 1)

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


    def test_select_clausePoints_by_note_id(self):
        with app.app_context():
            try:
                result = sqlalchemy_orm.get_item_from_db(ClausePoints, {'note_id':1, 'clause_id':1})
                self.assertIsNotNone(result)
                self.assertIsInstance(result, list)
                self.assertNotEqual(len(result), 0)
                self.assertEqual(result[0]['note_id'], 1)
                self.assertEqual(result[0]['clause_id'], 1)

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


if __name__ == '__main__':
    unittest.main()