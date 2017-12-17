import sqlite3
from flask import g

from studi import app
from studi import module_path

DBPATH = module_path + '/db/studi.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DBPATH)
        app.logger.debug(DBPATH)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def update_db(query, commit=False, one=False):
    cur = get_db().execute(query)
    if commit:
        get_db().commit()
    rowcount = cur.rowcount
    cur.close()
    return rowcount