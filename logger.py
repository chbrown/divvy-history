import sys
import logging
logger = logging.getLogger('divvy')

# gunicorn uses loglevel from settings.py (the gunicorn.config file) to create two loggers:
#   gunicorn.error, with that loglevel, pointed at STDERR (or STDOUT?)
#   gunicorn.access, with that loglevel + 10, pointed at STDOUT
gunicorn_error = logging.getLogger('gunicorn.error')
if gunicorn_error.level != 0 and len(gunicorn_error.handlers):
    # inherit from gunicorn logger, if it exists
    # basically just copy over the important stuff from the gunicorn.error logger
    [logger.addHandler(handler) for handler in gunicorn_error.handlers]
    logger.setLevel(gunicorn_error.level)
else:
    from settings import loglevel
    # CRITICAL 50
    # ERROR    40
    # WARNING  30
    # INFO     20
    # DEBUG    10
    # NOTSET    0
    # this level is the minimum that this logger will print
    level = getattr(logging, loglevel.upper())
    logger.setLevel(level)

    # use STDERR
    stderr_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(stderr_handler)

logger.info('Logger loaded: %s at level %d (%s)', logger.name, logger.level, logging.getLevelName(logger.level))
