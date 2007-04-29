from econ.www.tests import *


class TestGraph(TestControllerTwill):

    def test_test(self):
        offset = url_for(controller='graph', action='test')
        url = self.siteurl + offset
        web.go(url)
        web.code(200)
        print web.show()
        web.title('Graph - Chart')
        web.find('1')

    def test_index(self):
        offset = url_for(controller='graph')
        dataurl = 'http://p.knowledgeforge.net/econ/svn/trunk/data/world_population_historical/data.csv'
        url = self.siteurl + offset + '?data_url=%s' % dataurl
        web.go(url)
        web.code(200)
        print web.show()
        web.title('Graph - Chart')
        web.find('Kremer')

    def test_help(self):
        offset = url_for(controller='graph', action='help')
        url = self.siteurl + offset
        web.go(url)
        web.code(200)
        print web.show()
        web.find('To use this service')
    
    def test_raw(self):
        offset = url_for(controller='graph', action='source')
        dataurl = 'http://p.knowledgeforge.net/econ/svn/trunk/data/world_population_historical/data.csv'
        url = self.siteurl + offset + '?data_url=%s' % dataurl
        web.go(url)
        web.code(200)
        print web.show()
        web.find('<script')

