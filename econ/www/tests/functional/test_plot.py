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
        print offset
        table = \
'''0,1
1,0'''
        values = { 'data' : table }
        res = self.app.post(offset, values)
        print res
        assert '[0.0, 1.0], [1.0, 0.0]' in res

    # TODO: 2009-07-31 disabling this test
    # Re-enable if we can sort out wsgi_intercept (o/w remove permanently)
    def _test_chart_data_url(self):
        # you might think you could just use self.app for the wsgiapp (or even
        # self.app.app -- the original unwrapped wsgi app) but oh no something
        # weird is going on with the environ and all hell breaks loose
        # add_urllib2_intercept(appfunc=lambda: self.app.app)
        try:
            import wsgi_intercept
        except:
            msg = 'WARNING: not running test_chart_data_url as wsgi_intercept not installed.'
            raise Exception(msg)
        add_urllib2_intercept(appfunc=lambda: proxy_csv_app)
        offset = url_for(controller='plot', action='chart')
        # the url here does not matter because we have inserted a proxy which
        # always returns the same thing
        dataurl = 'http://p.knowledgeforge.net/econ/svn/trunk/data/world_population_historical/data.csv'
        url = offset + '?data_url=%s' % dataurl
        res = self.app.get(url)
        print str(res)
        assert 'Plot - Chart' in res
        assert 'Kremer' in res

    def test_chart_post(self):
        offset = url_for(controller='plot', action='chart')
        table = \
'''0,1
1,0'''
        values = { 'data' : table }
        res = self.app.post(offset, values)
        assert '<table' in res
        assert '1' in res


def add_urllib2_intercept(appfunc, host='localhost', port=80):
    '''Add urllib2 intercept.
    
    NB: this needs wsgi_intercept code for urllib2. This was in:
    
    http://darcs.idyll.org/~t/projects/wsgi_intercept/README.html

    Now part of wsgi_intercept: easy_install wsgi_intercept

    @param appfunc: function that returns the WSGI app.
    '''
    from wsgi_intercept.urllib2_intercept import install_opener
    install_opener()

    import wsgi_intercept
    wsgi_intercept.add_wsgi_intercept(host, port, appfunc)

    wsgi_intercept.add_wsgi_intercept('some_host', 80, appfunc)


def proxy_csv_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type','text/plain')]
    start_response(status, response_headers)
    out = \
'''Year,Kremer
1850,10.9
1851,10.6
1852,10.6
'''
    return [out]

