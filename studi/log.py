import os
import studi
import logging
from flask import request

def gen_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(os.path.join(studi.app.config['LOG_DIR'], module_name + '.log'))
    logger_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
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