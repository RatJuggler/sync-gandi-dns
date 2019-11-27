"""
Add a custom VERBOSE logging level between DEBUG and INFO.
"""
import logging

VERBOSE = 15
VERBOSE_NAME = "VERBOSE"


def verbose(msg, *args, **kwargs) -> None:
    """
    Verbose logging function.
    :param msg: The message to log as verbose
    :param args: Standard args
    :param kwargs: Standard kwargs
    :return: No meaningful return
    """
    if logging.getLogger().isEnabledFor(VERBOSE):
        logging.log(VERBOSE, msg)


logging.addLevelName(VERBOSE, VERBOSE_NAME)
logging.verbose = verbose
logging.Logger.verbose = verbose


def configure_logging(loglevel: str) -> None:
    """
    Configure basic logging to the console.
    :param loglevel: level name from the command line or default
    :return: No meaningful return
    """
    if logging.getLevelName(loglevel) == "Level {0}".format(loglevel):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=loglevel, format='%(asctime)s - %(levelname)s - %(message)s')
