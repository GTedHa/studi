import logging
import os
import unittest

import studi


def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(studi.app.config['LOG_DIR'], test_name + '.log'))
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger

test_name = 'test_create_db'
logger = gen_logger(test_name)


class TestCreateDB(unittest.TestCase):

    def setUp(self):
        studi.app.testing = True
        self.app = studi.app.test_client()

    def test_connect_db(self):
        with studi.app.app_context():
            try:
                db = studi.intf_db.get_db()
            except:
                logger.debug("Cannot get db..")
                db = None
            self.assertIsNotNone(db)

    def test_create_table_notes(self):
        with studi.app.app_context():
            try:
                db = studi.intf_db.get_db()
            except:
                logger.debug("Cannot get db..")
                db = None
            self.assertIsNotNone(db)
            executed = studi.utils.execute_sql_file(
                studi.module_path + '/db/Notes.sql',
                db
            )
            self.assertTrue(executed)

    def test_create_table_clauses(self):
        with studi.app.app_context():
            try:
                db = studi.intf_db.get_db()
            except:
                logger.debug("Cannot get db..")
                db = None
            self.assertIsNotNone(db)
            executed = studi.utils.execute_sql_file(
                studi.module_path + '/db/Clauses.sql',
                db
            )
            self.assertTrue(executed)

    def test_create_table_clause_points(self):
        with studi.app.app_context():
            try:
                db = studi.intf_db.get_db()
            except:
                logger.debug("Cannot get db..")
                db = None
            self.assertIsNotNone(db)
            executed = studi.utils.execute_sql_file(
                studi.module_path + '/db/ClausePoints.sql',
                db
            )
            self.assertTrue(executed)


if __name__ == '__main__':
    unittest.main()
