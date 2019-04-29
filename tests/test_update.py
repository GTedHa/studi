import logging
import os
import unittest

from studi import app
from studi import sqlalchemy
from studi import upload
from studi.sqlalchemy import Notes, Clauses, ClausePoints

def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(app.config['LOG_DIR'], test_name + '.log'))
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
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

        #create new tesint DB & insert dummy data
        if os.path.exists("../studi/db/test_studi.db"):
            sqlalchemy.drop_db(False)
        sqlalchemy.create_db(False)
        upload.insert_csv_to_db(False)  # note_id : 1
        upload.insert_csv_to_db(False)  # note_id : 2
        upload.insert_csv_to_db(False)  # note_id : 3


    def test_update_note_name(self):
        with app.app_context():
            try:
                sqlalchemy.update_data_to_db(Notes, {'note_id' : 1}, {'note_name' : '새로운 노트 이름'})
            except Exception as exc:
                logger.debug("Cannot UPDATE notename, Error: {0}".format(exc))
            finally:
                result = sqlalchemy.get_item_from_db(Notes, {'note_id' : 1})
                result = result[0]
                self.assertEqual(result['note_name'], '새로운 노트 이름')


    def test_update_clauses(self):
        with app.app_context():
            try:
                sqlalchemy.update_data_to_db(Clauses, {'note_id' : 1, 'clause_id' : 2}, {'title': '바뀐 제목', 'contents' : "바뀐 내용"})
            except Exception as exc:
                logger.debug("Cannot UPDATE clause(title, contents), Error: {0}".format(exc))
            finally:
                result = sqlalchemy.get_item_from_db(Clauses, {'note_id' : 1, 'clause_id':2})
                result = result[0]
                self.assertEqual(result['title'], '바뀐 제목')
                self.assertEqual(result['contents'], '바뀐 내용')


    def test_update_clausePoints(self):
        with app.app_context():
            try:
                sqlalchemy.update_data_to_db(ClausePoints, {'clause_id' : 3}, {'imp' : 1, 'und' : 2})
            except Exception as exc:
                logger.debug("Cannot UPDATE clausePoints(imp, und), Error: {0}".format(exc))
            finally:
                result = sqlalchemy.get_item_from_db(ClausePoints, {'clause_id' : 3})
                result = result[0]
                self.assertEqual(result['imp'], 1)
                self.assertEqual(result['und'], 2)


if __name__ == "__main__":
    unittest.main()