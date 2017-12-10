import logging
import sqlite3

from studi import app

def execute_sql_file(file_name, cur):
    try:
        fd = open(file_name, 'r')
        sql_file = fd.read()
        fd.close()
    except Exception:
        # Read file error.
        app.logger.warning("Cannot open(read) .sql file.")
        return False
    try:
        cur.executescript(sql_file)
    except sqlite3.Error:
        # Execute error.
        app.logger.warning("Fail to execute {0}".format(file_name))
        return False
    return True