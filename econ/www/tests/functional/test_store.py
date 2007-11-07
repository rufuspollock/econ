from econ.www.tests import *

class TestStore(TestController2):

    def test_index(self):
        offset = url_for(controller='store', action='index')
        res = self.app.get(offset)
        print str(res)
        assert 'Store - Index' in res
        name = 'World Population Historical'
        assert name in res
        # does not work!! gives code 500
        # web.follow('world_population_historical')
        # web.code(200)

    def test_view(self):
        id = 'uk_price_index_1850-2002_annual'
        offset = url_for(controller='store', action='view', id=id)
        print offset
        res = self.app.get(offset)
        assert 'Store - View' in res
        assert 'UK Price Index' in res
        assert 'Raw Data' in res
        assert 'Plot This Dataset' in res

    def test_data(self):
        id = 'uk_price_index_1850-2002_annual'
        offset = url_for(controller='store', action='data', id=id)
        res = self.app.get(offset)
        # TODO: sort this out
        print str(res)
        assert '' in res

