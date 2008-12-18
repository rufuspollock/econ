import genshi

from econ.www.lib.base import *

import econdata.ukgovfinances.data as d
import econ.data

class WdmmgController(BaseController):

    def index(self):
        return render('wdmmg/index')

    def spend(self):
        a = d.Analyzer()
        entries, years = a.extract_simple()
        expenditure = entries['Public sector current expenditure']
        import econ.data
        td = econ.data.TabularData(
                header=['Year'],
                data=[years]
                )
        for k,v in entries.items():
            td.header.append(k)
            td.data.append(v)
        td.data = econ.data.transpose(td.data)

        import econ.www.controllers.plot
        plotctr = econ.www.controllers.plot.PlotController()
        c.html_table = genshi.XML(plotctr.get_html_table(td))
        c.chart_code = genshi.HTML(plotctr._get_chart_code(td))
        c.fig_title = u'UK Government Expenditure (Millions)'
        return render('wdmmg/spend')

    def dept(self):
        a = d.Analyzer()
        data = a.extract_dept_spend()
        # create bar positions at 1,2,3,...
        count = 1
        c.datasets = []
        for k in data:
            c.datasets.append(
                {'label': k,
                 'data': [[ count, data[k] ]]
                 }
                )
            count += 1
        import simplejson as sj
        # won't plot more than 5 or so items with bars ...
        c.datasets = sj.dumps(c.datasets[:30])
        c.fig_title = 'UK Government Spending by Dept (2007)'
        return render('wdmmg/dept')

