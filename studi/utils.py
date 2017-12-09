import logging
from sqlite3 import OperationalError

from studi import app

def execute_sql(file_name, cur):
    fd = open(file_name, 'r')
    sql_file = fd.read()
    fd.close()

    sql_commands = sql_file.split(';')
    app.logger.debug(sql_commands)
    exe_cnt = 0
    for command in sql_commands:
        try:
            cur.execute(command)
            app.logger.debug("Success to call command: {0}".format(command))
            exe_cnt += 1
        except OperationalError as ope:
            app.logger.debug("Fail to call command: {0}".format(command))
            break
    return (exe_cnt, len(sql_commands))