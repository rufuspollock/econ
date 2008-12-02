from econ.www.tests import *

class TestRoot(TestController2):

    def test_index(self):
        res = self.app.get('/')
        print str(res)
        assert 'Open Economics - Home' in res

    def test_current_value(self):
        offset = '/current_value/?year=1900'
        res = self.app.get(offset)
        print str(res)
        assert 'Current Value' in res
        assert 'Value of one pound from 1900 in 2002 was: 71.65' in res

