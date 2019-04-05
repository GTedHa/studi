import os
from flask import Flask

module_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config.from_object('studi.default_settings')
try:
    app.config.from_envvar('STUDI_SETTINGS')
except RuntimeError:
    pass

if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler
    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'studi.log'), 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)
else:
   import logging
   from logging import FileHandler
   # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
   file_handler = FileHandler(os.path.join(app.config['LOG_DIR'], 'studi_debug.log'))
   file_handler.setLevel(logging.DEBUG)
   file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
   app.logger.addHandler(file_handler)


import studi.intf_db
import studi.rest_apis
import studi.upload
import studi.utils
import studi.views
import studi.sqlite_db
