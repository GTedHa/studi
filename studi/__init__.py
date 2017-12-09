import os
from flask import Flask

module_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config.from_object('studi.default_settings')
app.config.from_envvar('STUDI_SETTINGS')

if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler
    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'studi.log'), 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)

import studi.views
import studi.rest_apis
import studi.intf_db
import studi.utils
