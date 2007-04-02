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

    def test_store(self):
        offset = '/store'
        url = self.siteurl + offset
        web.go(url)
        print web.show()
        web.title('Store Index')
        web.code(200)

    def test_view_raw(self):
        offset = '/store'
        url = self.siteurl + offset
        web.go(url)
        # first on list
        web.follow('Raw')
        web.find('1694-10-01,6')
        web.code(200)

    def test_view_html(self):
        offset = '/store'
        url = self.siteurl + offset
        web.go(url)
        # first on list
        web.follow('uk_interest_rates')
        web.code(200)
        print web.show()
        web.title('View Dataset \(html\)')
        web.find('1694-10-01')

