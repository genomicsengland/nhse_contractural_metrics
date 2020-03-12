"""
creates the console and file handlers for logging
file handler is a timed rotating handler (currently rotating each day) and
keeping backups
"""
import logging
import logging.config
import logging.handlers
import os

def setup_logger():
    """
    set up logging handlers and formatters
    """

    # set up log directory if it doesn't exist
    log_dir = 'log'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # log config
    log_config = {
        'version': 1,
        'formatters': {
            'fFormatter': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'cFormatter': {
                'class': 'logging.Formatter',
                'format': '%(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'cFormatter'
            },
            'fileHandler': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': 'log/ngis-mq.log',
                'formatter': 'fFormatter',
                'when': 'd',
                'interval': 1,
                'backupCount': 7
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler', 'fileHandler']
        }
    }
    logging.config.dictConfig(log_config)
