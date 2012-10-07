import sys
import os
import logging
import logging.handlers

def trace(func):
    def wrapper(self, *args):
        self.logger.info("enter into %s, params %s" % (func.__name__, str(args)))
        s = func(self, *args)
        self.logger.info("%s returned: %s" % (func.__name__, str(s)))
        return s
    return wrapper

class LOG:
    
    logger = None
    logfile = "loginfo.log"
    loglevel = logging.INFO
    
    def __init__(self, logfile = None, loglevel= None):
        if logfile:
            LOG.logfile = logfile
        if loglevel:
            LOG.loglevel = loglevel

    @staticmethod 
    def getlogger():
        
        if not LOG.logger:
            logger = logging.getLogger()
            logger.setLevel(LOG.loglevel)

            handler = logging.handlers.RotatingFileHandler(LOG.logfile, maxBytes=4096000, backupCount=5)
            formatter = logging.Formatter("%(asctime)s %(levelname)s [%(thread)d@%(threadName)s] (%(filename)s:%(lineno)d) - %(message)s") 
            handler.setFormatter(formatter)

            logger.addHandler(handler)
            LOG.logger = logger
 
        return LOG.logger

    def __del__(self):
        pass

def test():
    test_log = LOG("test.log") 
    logger = test_log.getlogger()
    
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")
    logger.debug("debug message")

if __name__ == '__main__':
    test()
