import os
import urllib
import StringIO

from econ.www.lib.base import *

import econ.store

class RootController(BaseController):

    def index(self):
        return render('index')

    def current_value(self):
        c.error_message = ''
        try:
            year = int(request.params.get('year', 2001))
            currentValue = get_current_value(year)
            c.year = year,
            c.ownPath = '/current_value/'
            c.value = currentValue
            c.data_url = h.url_for(controller='store', action='view',
                    id='uk_price_index_1850-2002_annual')
        except Exception, inst:
            c.error_message = str(inst)
        return render('current_value')

def get_current_value(startYear, endYear=2002):
    import econ.data
    import econ.model.discount
    package = econ.store.index().get('uk_price_index_1850-2002_annual')
    filePath = econ.store.get_data_path(package)
    ts1 = econ.data.getTimeSeriesFromCsv(file(filePath))
    discounter = econ.model.discount.DiscountRateHistorical(ts1)
    return discounter.getReturn(startYear, endYear)

