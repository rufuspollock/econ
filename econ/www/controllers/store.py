import os
import urllib
import StringIO

from econ.www.lib.base import *

import econ
import econ.store

class StoreController(BaseController):

    def index(self):
        import econ.store
        index = econ.store.index()
        packages = [ pkg for pkg in index.list() ]
        storeIndex = []
        for package in packages:
            title = package.metadata.get('title', 'No title available')
            storeIndex.append((h.url_for(controller='store', action='view',
                id=package.name), title))
        c.store_index = storeIndex
        def mycmp(x,y):
            return cmp(x[1], y[1])
        c.store_index.sort(mycmp)
        return render('store/index')

    def _get_package(self, id):
        if id is None:
            msg = 'Please provide a package id.'
            raise Exception(msg) 
        import econ.store
        index = econ.store.index()
        try:
            package = index.get(id)
        except:
            msg = 'The store does not contain a data package with id: %s' % id
            raise Exception(msg) 
        return package

    def view(self, id):
        c.pkg = self._get_package(id)
        # limit to a maximum to avoid problems with huge datasets
        data_limit = 1000
        c.plot_data_url = h.url_for(controller='plot', action='chart', id=id,
                limit='[:%s]' % data_limit)
        c.data_url = h.url_for(controller='store', action='data', id=id)
        return render('store/view')

    def data(self, id):
        package = self._get_package(id)
        try:
            fileobj = file(package.data_path)
            result = fileobj.read()
        except:
            result = 'It looks like there is no data file for this dataset'
        response.headers['Content-Type'] = 'text/plain'
        return result

    def create(self):
        pass
        
