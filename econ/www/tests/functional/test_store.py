from econ.www.tests import *

from econ.www.controllers.root import parse_limit, limit_fileobj
from StringIO import StringIO

class TestStore(TestControllerTwill):

    def test_index(self):
        offset = url_for(controller='store', action='index')
        url = self.siteurl + offset
        web.go(url)
        print web.show()
        web.title('Store Index')
        web.code(200)

