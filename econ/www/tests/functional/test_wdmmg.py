from econ.www.tests import *

class TestStore(TestController2):
    def test_index(self):
        offset = url_for(controller='wdmmg', action='index')
        res = self.app.get(offset)
        assert 'Where Does My Money Go' in res

    def test_cra(self):
        offset = url_for(controller='wdmmg', action='cra')
        res = self.app.get(offset)
        assert 'CRA' in res
        
        form = res.forms[0]
        title = '6. Housing and community amenities'
        form['q'] = title
        res = form.submit()
        assert 'matches found' in res
        assert title in res

        res = res.click('LA Dummy sprog 6. Housing and community amenities - ENGLAND_North East', index=0)
        assert 'Graph' in res


    def test_myseries(self):
        offset = url_for(controller='wdmmg', action='myseries')
        res = self.app.get(offset)
        assert 'My Series' in res

