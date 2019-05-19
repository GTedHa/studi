import os
from flask import Flask

module_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config.from_object('studi.config')


import studi.upload
import studi.views
import studi.sqlalchemy_orm
import studi.log
import studi.rest_apis
import studi.custom_error

if not os.path.exists('studi/db/studi.db'):
    studi.sqlalchemy_orm.create_db(True)
