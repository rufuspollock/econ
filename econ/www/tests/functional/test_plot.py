from econ.www.tests import *


class TestPlot(TestController2):

    def test_test(self):
        offset = url_for(controller='plot', action='test')
        res = self.app.get(offset)
        print str(res)
        assert 'Plot - Chart' in res
        assert '1' in res

    def test_help(self):
        offset = url_for(controller='plot', action='help')
        res = self.app.get(offset)
        print str(res)
        assert 'provides plotting functionality' in res
    
    def test_source(self):
        offset = url_for(controller='plot', action='source')
        dataurl = 'http://p.knowledgeforge.net/econ/svn/trunk/data/world_population_historical/data.csv'
        url = offset + '?data_url=%s' % dataurl
        res = self.app.get(url)
        print str(res)
        assert '<script' in res

    def test_index_data_url(self):
        offset = url_for(controller='plot')
        dataurl = 'http://p.knowledgeforge.net/econ/svn/trunk/data/world_population_historical/data.csv'
        url = offset + '?data_url=%s' % dataurl
        res = self.app.get(url)
        print str(res)
        assert 'Plot - Chart' in res
        assert 'Kremer' in res

    def test_index_post(self):
#        # add intercept for urllib2
#        add_urllib2_intercept(self.host, self.port, lambda : self.wsgiapp)
#        offset = url_for(controller='plot')
#        url = self.siteurl + offset
#        table = \
#'''0,1
#1,0'''
#        values = { 'data' : table }
#        response = do_post(url, values)
#        the_page = response.read()
#        assert '<table' in the_page
#        assert '1' in the_page
        offset = url_for(controller='plot')
        table = \
'''0,1
1,0'''
        values = { 'data' : table }
        # TODO: resolve the issues with this ...
        # res = self.app.post(offset, values)
        # assert '<table' in res
        # assert '1' in res

#def add_urllib2_intercept(host, port, appfunc):
#    # NB: this needs wsgi_intercept code for urllib2
#    # http://darcs.idyll.org/~t/projects/wsgi_intercept/README.html
#    # appfunc should be a function that returns the WSGI app
#    import wsgi_urllib2
#    import wsgi_intercept
#    wsgi_intercept.add_wsgi_intercept(host, port, appfunc)
#    wsgi_urllib2.install_opener()
#
#def do_post(url, data):
#    # data should be a dictionary of POST values
#    import urllib
#    import urllib2
#    postdata = urllib.urlencode(data)
#    req = urllib2.Request(url, postdata)
#    response = urllib2.urlopen(req)
#    return response
#
