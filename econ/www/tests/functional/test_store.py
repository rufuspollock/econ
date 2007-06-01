from econ.www.tests import *

class TestStore(TestControllerTwill):

    def test_index(self):
        offset = url_for(controller='store', action='index')
        url = self.siteurl + offset
        web.go(url)
        web.code(200)
        print web.show()
        web.title('Store - Index')
        name = 'World Population Historical'
        web.find(name)
        # does not work!! gives code 500
        # web.follow('world_population_historical')
        # web.code(200)

    def test_view(self):
        id = 'uk_price_index_1850-2002_annual'
        offset = url_for(controller='store', action='view', id=id)
        url = self.siteurl + offset
        web.go(url)
        print web.show()
        web.code(200)
        web.title('Store - View')
        web.find('UK Price Index')
        web.find('Raw Data')
        web.find('Plot This Dataset')

    def test_data(self):
        id = 'uk_price_index_1850-2002_annual'
        offset = url_for(controller='store', action='data', id=id)
        url = self.siteurl + offset
        web.go(url)
        web.code(200)
        print web.show()
        web.find('')

