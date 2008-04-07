from econ.data.misc import *

def test_floatify():
    x = '10'
    assert floatify(x) == 10.0

def test_floatify_matrix():
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
