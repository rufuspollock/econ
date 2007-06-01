from StringIO import StringIO
from econ.www.controllers.plot import parse_limit, limit_fileobj

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



