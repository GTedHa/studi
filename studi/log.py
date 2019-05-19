import os
from studi import app
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import request

def gen_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    if app.config['TESTING']:
        # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
        file_handler = TimedRotatingFileHandler(os.path.join(app.config['TEST_LOG_DIR'], 'studi_debug.log'),
                                                'midnight')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
        logger.addHandler(file_handler)
        return logger

    if app.config['ENV'] == 'production':
        file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'studi.log'), 'midnight')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
        logger.addHandler(file_handler)
    else:
        file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'studi_debug.log'), 'midnight')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
        logger.addHandler(file_handler)

    return logger


def logger_decorator_with_params(logger):
    def wrapper(func):
        def decorator(*args, **kwargs):
            logger.info('REQUEST, {0}, params : {1}'.format(request.environ['werkzeug.request'], kwargs))
            result = func(*args, **kwargs)
            logger.info("RESPONSE, {0}".format(result))
            return result
        return decorator
    return wrapper

logger = gen_logger('studi')
