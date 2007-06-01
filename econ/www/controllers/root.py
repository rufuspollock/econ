import os
import urllib
import StringIO

from econ.www.lib.base import *

import econ
cfg = econ.conf

class RootController(BaseController):

    def index(self):
        return render_response('index')

    def current_value(self):
        try:
            year = int(request.params.get('year', 2001))
            currentValue = get_current_value(year)
            c.year = year,
            c.ownPath = '/current_value/'
            c.value = currentValue
            return render_response('current_value')
        except Exception, inst:
            return Response('<p><strong>There was an error: ' +  str(inst) + '</strong></p>')

def get_current_value(startYear, endYear=2002):
    import econ.data
    import econ.store
    import econ.DiscountRate
    databundle = econ.store.index()['uk_price_index_1850-2002_annual']
    filePath = databundle.data_path
    ts1 = econ.data.getTimeSeriesFromCsv(file(filePath))
    discounter = econ.DiscountRate.DiscountRateHistorical(ts1)
    return discounter.getReturn(startYear, endYear)

