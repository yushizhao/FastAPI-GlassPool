import logging
import functools

def start_log(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
 
    rht = logging.handlers.TimedRotatingFileHandler(f"{name}.log", 'D')
    fmt = logging.Formatter("%(asctime)s %(filename)s %(lineno)s \
      %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
    rht.setFormatter(fmt)
    logger.addHandler(rht)

    return logger

glassflow_log = start_log("glassflow")

def glassflow(func):
    @functools.wraps(func)
    def glassflow_decorator(*args, **kwargs):
        # Do something before
        glassflow_log.info(args, kwargs)
        value = func(*args, **kwargs)
        # Do something after
        glassflow_log.info(value)
        return value
    return glassflow_decorator