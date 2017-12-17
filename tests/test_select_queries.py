import collections
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

test_name = 'test_select_queries'
logger = gen_logger(test_name)


class TestSelectQueries(unittest.TestCase):

    def setUp(self):
        studi.app.testing = True
        self.app = studi.app.test_client()

    def test_select_all_notes(self):
        with studi.app.app_context():
            try:
                rv = studi.intf_db.query_db(
                    "SELECT * FROM Notes"
                )
            except Exception:
                rv = None
        self.assertIsNotNone(rv)
        if rv:
            if isinstance(rv, collections.Iterable):
                for item in rv:
                    logger.debug('{0} | {1} '.format(item['note_id'], item['note_name']))
            else:
                logger.debug('{0} | {1} '.format(rv['note_id'], rv['note_name']))

    def test_select_all_clauses(self):
        with studi.app.app_context():
            try:
                rv = studi.intf_db.query_db(
                    "SELECT * FROM Clauses"
                )
            except Exception:
                rv = None
        self.assertIsNotNone(rv)
        if rv:
            if isinstance(rv, collections.Iterable):
                for item in rv:
                    logger.debug('{0} | {1} | {2} | {3}'.format(
                        item['note_id'],
                        item['clause_id'],
                        item['title'],
                        item['contents']
                    ))
            else:
                logger.debug('{0} | {1} | {2} | {3}'.format(
                        rv['note_id'],
                        rv['clause_id'],
                        rv['title'],
                        rv['contents']
                    ))

    def test_select_all_clause_points(self):
        with studi.app.app_context():
            try:
                rv = studi.intf_db.query_db(
                    "SELECT * FROM ClausePoints"
                )
            except Exception:
                rv = None
        self.assertIsNotNone(rv)
        if rv:
            if isinstance(rv, collections.Iterable):
                for item in rv:
                    logger.debug('{0} | {1} | {2} | {3}'.format(
                        item['clause_id'],
                        item['note_id'],
                        item['imp'],
                        item['und']
                    ))
            else:
                logger.debug('{0} | {1} | {2} | {3}'.format(
                        rv['clause_id'],
                        rv['note_id'],
                        rv['imp'],
                        rv['und']
                    ))

if __name__ == '__main__':
    unittest.main()
