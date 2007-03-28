from StringIO import StringIO

import twill
from twill import commands as web

import econ.www.plainwsgi


class TestSite:

    port = 8080
    siteurl = 'http://localhost:8080/'

    def setup_method(self, name=''):
        wsgi_app = econ.www.plainwsgi.EconWebInterface()
        twill.add_wsgi_intercept('localhost', self.port, lambda : wsgi_app)
        self.outp = StringIO()
        twill.set_output(self.outp)

    def teardown_method(self, name=''):
        # remove intercept.
        twill.remove_wsgi_intercept('localhost', self.port)

    def test_index(self):
        web.go(self.siteurl)
        print web.show()
        web.code(200)
        web.title('Open Economics Index')

    def test_current_value(self):
        offset = 'current_value'
        url = self.siteurl + offset
        web.go(url)
        print web.show()
        web.code(200)
        web.find('Current Value')

    def test_store(self):
        offset = 'store'
        url = self.siteurl + offset
        web.go(url)
        print web.show()
        web.title('Store Index')
        web.code(200)

    def test_view_html(self):
        offset = 'store/view/'
        url = self.siteurl + offset
        web.go(url)
        print web.show()
        web.code(200)
