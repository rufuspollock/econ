from econ.www.lib.base import *

import econdata.ukgovfinances.data as d

class WdmmgController(BaseController):

    def index(self):
        return render('wdmmg/index')

    def spend(self):
        a = d.Analyzer()
        data = a.extract_dept_spend()
        entries, years = a.extract_simple()
        expenditure = entries['Public sector current expenditure']
        d1 = [ map(lambda x: [x[0], x[1]], zip(years, expenditure)) ]
        c.datasets = [ d1 ]
        c.fig_title = 'UK Government Expenditure'
        return render('wdmmg/spend')

    def dept(self):
        pass

