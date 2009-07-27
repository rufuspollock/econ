import os

import genshi

from econ.www.lib.base import *

import econdata.ukgovfinances.data as d
import econ.data
import econdata.ukgovfinances.db

class WdmmgController(BaseController):
    dbmod = econdata.ukgovfinances.db
    dbpath = os.path.join(config['db_store_path'], 'ukgovfinances.db')
    dburi = 'sqlite:///%s' % dbpath

    def __before__(self):
        self.dbmod.Session.clear()
        self.repo = self.dbmod.Repository(self.dburi)

    def __after__(self):
        self.dbmod.Session.remove()

    def index(self):
        c.tables = self.dbmod.PesaTable.query.all()
        return render('wdmmg/index')

    def table(self, id=None):
        if id is None:
            abort(404)
        c.table = self.dbmod.PesaTable.query.get(int(id))
        if c.table is None:
            abort(404)
        c.expenditures = self.dbmod.Expenditure.query.\
                filter_by(pesatable=c.table).\
                order_by(self.dbmod.Expenditure.title).\
                order_by(self.dbmod.Expenditure.date).all()
        # from formalchemy import FieldSet, Field, Grid
        # c.grid = Grid(self.dbmod.Expenditure, c.expenditures).render()
        # c.grid = genshi.HTML(c.grid)
        # fs = FieldSet(c.table)
        import econ.data
        td = econ.data.TabularData()
        td.header = ['Year', 'Title', 'Amount']
        td.data = [ [ e.date, e.title, e.amount] for e in c.expenditures ]
        tdout = econ.data.pivot(td,'Year','Title','Amount')
        tdouttable = econ.data.pivot(td,'Title','Year','Amount')

        import econ.www.controllers.plot
        plotctr = econ.www.controllers.plot.PlotController()
        c.html_table = genshi.XML(plotctr.get_html_table(tdouttable))
        c.chart_code = genshi.HTML(plotctr._get_chart_code(tdout))

        return render('wdmmg/table')

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
        h.redirect_to(controller='wdmmg', action='overview', id='department')

    def overview(self, id=None):
        order = id
        if not order: order='department'
        a = d.Analyzer()
        # data = a.extract_dept_spend_for_jit()
        data = a.department_and_function(order)
        c.json = data
        if order == 'department':
            c.fig_title = 'UK Government Spending by Department then Function (2008)'
        else:
            c.fig_title = 'UK Government Spending by Function then Department (2008)'
        return render('wdmmg/dept')

