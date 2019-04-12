import logging
import os
import unittest
from studi import app
from studi import upload

import studi
from studi import sqlite_db


def gen_logger(test_name):
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(studi.app.config['LOG_DIR'], test_name + '.log'))
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    return logger

test_name = "test_rest_api"
logger = gen_logger(test_name)

class TestRestAPI(unittest.TestCase):

    def setUp(self):
        studi.app.testing = True
        self.app = studi.app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'

        # create new testing db & insert dummy data
        if os.path.exists("../studi/db/test_studi.db"):
            sqlite_db.drop_db(False)
        self.db = sqlite_db.create_db(False)
        upload.insert_csv_to_db(False) # note_id : 1
        upload.insert_csv_to_db(False) # note_id : 2
        upload.insert_csv_to_db(False) # note_id : 3


if __name__ == "__main__":
    unittest.main()


