"""
Econ logger
"""

import logging
import logging.config
import logging.handlers
import os

import econ

cfg = econ.get_config()
application_name = econ.__application_name__

def get_logger():
    """
    Convenience method to get instance of a python logger named after the
    application
    """
    return logging.getLogger(application_name)
 
def init_logging_in_code():
    """
    Configure the logger system in code.
    Two loggers: root + application
    Two output sources: file + stderr
    Only log level at ERROR or above go to stderr
    Log level for output to file is configurable via logging.level

    REQUIRES: config variable log.level and log.file_path in config file.
    """
    logging_level = cfg['log.level']
    logging_log_file_path = cfg['log.file_path']
    logLevel = None 
    logLevels = {
        'DEBUG'    : logging.DEBUG,
        'INFO'     : logging.INFO,
        'WARNING'  : logging.WARNING,
        'ERROR'    : logging.ERROR,
        'CRITICAL' : logging.CRITICAL
    }
    if logging_level in logLevels:
        logLevel = logLevels[logging_level]
    else:
        raise "Logging level not in valid list: %s" % " ".join(logLevels.keys())
    
    consoleFormat = '%(name)s [%(levelname)s] %(message)s'
    consoleFormatter = logging.Formatter(consoleFormat)
    fileFormat = '[%(asctime)s] %(message)s'
    fileFormatter = logging.Formatter(fileFormat)
    
    consoleHandler = logging.StreamHandler()
    # have to set level here since does not seem to work when set on logger
    consoleHandler.setLevel(logging.ERROR)
    fileHandler = logging.handlers.RotatingFileHandler(
        logging_log_file_path,
        mode='a+',
        maxBytes=10000000,
        backupCount=5
    )
    consoleHandler.setFormatter(consoleFormatter)
    fileHandler.setFormatter(fileFormatter)
    fileHandler.setLevel(logLevel)
    
    rootLogger = logging.getLogger('')
    applicationLogger = logging.getLogger(application_name)
    rootLogger.addHandler(consoleHandler)
    applicationLogger.addHandler(fileHandler)
    # setting this level seems to have no effect
    # i.e. debug events from the application logger still get processed
    # so we have set level on handler above
    # rootLogger.setLevel(logging.ERROR)
    # still need to set this or we don't get anything below warning
    applicationLogger.setLevel(logLevel)

def init_logging_from_file():
    logging_config_file = cfg['__file__']
    logging.config.fileConfig(logging_config_file)
    
init_logging_from_file()
log = get_logger()
log.warning('Logging initialised.')


