import logging
import os
import sqlalchemy
import unittest

from studi import app
from studi import sqlalchemy_orm, util, custom_error

def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(app.config['TEST_LOG_DIR'], test_name + '.log'))
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
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'


        # delete db
        if os.path.exists("../studi/db/test_studi.db"):
            sqlalchemy_orm.drop_db(False)
            self.app = app.test_client()


    def test_create_db(self):
        with app.app_context():
            try:
                db = sqlalchemy_orm.create_db(False)
                table_names = db.engine.table_names()
                self.assertIn('notes', table_names)
                self.assertIn('clauses', table_names)
                self.assertIn('clause_points', table_names)

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


    def test_delete_db(self):
        with app.app_context():
            try:
                db = sqlalchemy_orm.drop_db(False)
                table_names = db.engine.table_names()
                self.assertEqual(table_names, [])
                self.assertEqual(len(table_names), 0)

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