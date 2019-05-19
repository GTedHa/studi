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


test_name = "test_update"
logger = gen_logger(test_name)

class TestUpdateDB(unittest.TestCase):
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


    def test_update_note_name(self):
        with app.app_context():
            try:
                sqlalchemy_orm.update_data_to_db(Notes, {'note_id' : 1}, {'note_name' : '새로운 노트 이름'})
                result = sqlalchemy_orm.get_item_from_db(Notes, {'note_id' : 1})
                result = result[0]
                self.assertEqual(result['note_name'], '새로운 노트 이름')

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


    def test_update_clauses(self):
        with app.app_context():
            try:
                sqlalchemy_orm.update_data_to_db(Clauses, {'note_id' : 1, 'clause_id' : 2}, {'title': '바뀐 제목', 'contents' : "바뀐 내용"})
                result = sqlalchemy_orm.get_item_from_db(Clauses, {'note_id' : 1, 'clause_id':2})
                result = result[0]
                self.assertEqual(result['title'], '바뀐 제목')
                self.assertEqual(result['contents'], '바뀐 내용')

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


    def test_update_clausePoints(self):
        with app.app_context():
            try:
                sqlalchemy_orm.update_data_to_db(ClausePoints, {'clause_id' : 3}, {'imp' : 1, 'und' : 2})
                result = sqlalchemy_orm.get_item_from_db(ClausePoints, {'clause_id' : 3})
                result = result[0]
                self.assertEqual(result['imp'], 1)
                self.assertEqual(result['und'], 2)

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