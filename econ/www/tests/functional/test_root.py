from econ.www.tests import *

class TestRoot(TestControllerTwill):

    def test_index(self):
        web.go(self.siteurl)
        print web.show()
        web.code(200)
        web.title('Open Economics Index')

    def test_current_value(self):
        offset = '/current_value/?year=1900'
        url = self.siteurl + offset
        web.go(url)
        print web.show()
        web.code(200)
        web.find('Current Value')
        web.find('Value of one pound from 1900 in 2002 was: 71.65')

