from econ.data.misc import *


class TestFloatify:
    def test_floatify_1(self):
        x = '10'
        assert floatify(x) == 10.0

    def test_floatify_2(self):
        x = '1,030'
        assert floatify(x) == 1030.0

    def test_floatify_matrix(self):
        x = [ 
                ['1', '2'],
                ['abc', '3.0']
                ]
        exp = [ 
                [1.0, 2.0],
                ['abc', 3.0]
                ]
        out = floatify_matrix(x)
        assert out == exp

