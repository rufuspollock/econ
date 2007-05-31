import os
import urllib
import StringIO

from econ.www.lib.base import *

import econ
cfg = econ.conf

class StoreController(BaseController):

    def index(self):
        import econ.store
        index = econ.store.index().items()
        def get_title(_dict):
            if _dict.has_key('title'):
                return _dict['title']
            else: return 'No title available'
        storeIndex = [ (ii[0], ii[1].metadata.get('title', 'No title available'), ii[1].data_path)
            for ii in index ]
        c.store_index = storeIndex
        return render_response('store_index')

    def create(self):
        pass
        
