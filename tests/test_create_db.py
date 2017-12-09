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
            exe_cnt, cmd_cnt = studi.utils.execute_sql(
                studi.module_path + '/db/Notes.sql',
                db
            )
            if cmd_cnt is 0 or exe_cnt is not cmd_cnt:
                logger.debug("Fail to create Notes table.")
            self.assertEqual(exe_cnt, cmd_cnt)

    def test_create_table_clauses(self):
        with studi.app.app_context():
            try:
                db = studi.intf_db.get_db()
            except:
                logger.debug("Cannot get db..")
                db = None
            self.assertIsNotNone(db)
            exe_cnt, cmd_cnt = studi.utils.execute_sql(
                studi.module_path + '/db/Clauses.sql',
                db
            )
            if cmd_cnt is 0 or exe_cnt is not cmd_cnt:
                logger.debug("Fail to create Clauses table.")
            self.assertEqual(exe_cnt, cmd_cnt)

    def test_create_table_clause_points(self):
        with studi.app.app_context():
            try:
                db = studi.intf_db.get_db()
            except:
                logger.debug("Cannot get db..")
                db = None
            self.assertIsNotNone(db)
            exe_cnt, cmd_cnt = studi.utils.execute_sql(
                studi.module_path + '/db/ClausePoints.sql',
                db
            )
            if cmd_cnt is 0 or exe_cnt is not cmd_cnt:
                logger.debug("Fail to create ClausePoints table.")
            self.assertEqual(exe_cnt, cmd_cnt)


if __name__ == '__main__':
    unittest.main()
