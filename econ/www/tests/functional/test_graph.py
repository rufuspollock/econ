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

    def test_help(self):
        offset = url_for(controller='graph', action='help')
        url = self.siteurl + offset
        web.go(url)
        web.code(200)
        print web.show()
        web.find('provides graphing functionality')
    
    def test_source(self):
        offset = url_for(controller='graph', action='source')
        dataurl = 'http://p.knowledgeforge.net/econ/svn/trunk/data/world_population_historical/data.csv'
        url = self.siteurl + offset + '?data_url=%s' % dataurl
        web.go(url)
        web.code(200)
        print web.show()
        web.find('<script')

    def test_index_data_url(self):
        offset = url_for(controller='graph')
        dataurl = 'http://p.knowledgeforge.net/econ/svn/trunk/data/world_population_historical/data.csv'
        url = self.siteurl + offset + '?data_url=%s' % dataurl
        web.go(url)
        web.code(200)
        print web.show()
        web.title('Graph - Chart')
        web.find('Kremer')

    def test_index_post(self):
        # add intercept for urllib2
        add_urllib2_intercept(self.host, self.port, lambda : self.wsgiapp)
        offset = url_for(controller='graph')
        url = self.siteurl + offset
        table = \
'''0,1
1,0'''
        values = { 'data' : table }
        response = do_post(url, values)
        the_page = response.read()
        assert '<table' in the_page
        assert '1' in the_page
        print the_page
        assert False

def add_urllib2_intercept(host, port, appfunc):
    # NB: this needs wsgi_intercept code for urllib2
    # http://darcs.idyll.org/~t/projects/wsgi_intercept/README.html
    # appfunc should be a function that returns the WSGI app
    import wsgi_urllib2
    import wsgi_intercept
    wsgi_intercept.add_wsgi_intercept(host, port, appfunc)
    wsgi_urllib2.install_opener()

def do_post(url, data):
    # data should be a dictionary of POST values
    import urllib
    import urllib2
    postdata = urllib.urlencode(data)
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
    return response

