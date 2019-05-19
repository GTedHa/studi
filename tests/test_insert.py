import logging
import os
import sqlalchemy
import unittest

from studi import app
from studi import sqlalchemy_orm, upload, util, custom_error


def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(app.config['TEST_LOG_DIR'], test_name + '.log'))
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
        self.app = app.test_client()
        # create new testing db
        if os.path.exists("../studi/db/test_studi.db"):
            sqlalchemy_orm.drop_db(False)
        self.db = sqlalchemy_orm.create_db(False)


    def test_insert_note_db(self):
        with app.app_context():
            try:
                Notes = sqlalchemy_orm.Notes
                note_id  = sqlalchemy_orm.insert_data_to_db('Notes', Notes('test_title_1'))
                self.assertIsNotNone(note_id)
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


    def test_insert_clause_db(self):
        with app.app_context():
            try:
                Clauses = sqlalchemy_orm.Clauses
                clauses_id = sqlalchemy_orm.insert_data_to_db('Clauses', Clauses(1, "test_clause_1", "test_content_1"))
                self.assertIsNotNone(clauses_id)
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


    def test_insert_clausePoints_db(self):
        with app.app_context():
            try:
                clausePoints = sqlalchemy_orm.ClausePoints
                # column = ['clause_id', 'note_id', 'imp', 'und']
                clausepoints_id = sqlalchemy_orm.insert_data_to_db("ClausePoints", clausePoints(1, 1))
                self.assertIsNotNone(clausepoints_id)
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


    def test_insert_csv_to_db(self):
        with app.app_context():
            if os.path.exists('../studi/uploads/studi_test_files.csv'):
                try:
                    note_id = upload.insert_csv_to_db()
                    self.assertIsNotNone(note_id)
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





