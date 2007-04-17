from econ.www.tests import *

from econ.www.controllers.root import parse_limit, limit_fileobj
from StringIO import StringIO

class TestMisc:

    def test_parse_limit(self):
        testvals = [
                ('[:]', (None,None)),
                ('[0:-1]', (0,-1)),
                ('[4:]', (4,None)),
                ('[4:10]', (4,10)),
                ]

        for pair in testvals:
            yield self._check, pair
    
    def _check(self, inpair):
        out = parse_limit(inpair[0])
        assert out == inpair[1]

    def test_limit_fileobj(self):
        xx = 'abc\nefg\nxyz\n'
        in_fo = StringIO(xx)
        out = limit_fileobj(in_fo, '[1:]')
        exp = 'efg\nxyz\n'
        assert exp == out.read()


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

    def test_view_html_limit(self):
        offset = '/view/'
        query = '?data_url=./data/uk_interest_rates/data.csv&format=html&limit=[6:10]'
        url = self.siteurl + offset + query
        web.go(url)
        web.code(200)
        print web.show()
        web.title('View Dataset \(html\)')
        web.notfind('1694-10-01')
        web.notfind('2001-10-04')
        web.find('1822-06-01')

