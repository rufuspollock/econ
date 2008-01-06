import econ.log

class TestLog(object):

    log = econ.log.get_logger()

    def testExists(self):
        assert self.log, "Logger isn't there!"
    
    def testLogDebug(self):
        self.log.debug('Debug logging test. Please ignore this message.')
    
    def testLogInfo(self):
        self.log.info('Info logging test. Please ignore this message.')
    
    def testLogWarning(self):
        self.log.warning('Warning logging test. Please ignore this message.')
    
    def testLogError(self):
        self.log.error('Error logging test. Please ignore this message.')
    
    def testLogCritical(self):
        self.log.critical('Critical logging test. Please ignore this message.')

