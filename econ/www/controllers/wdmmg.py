import os

import genshi
import swiss.tabular

from econ.www.lib.base import *
import econ.www.controllers.plot

import econdata.ukgov_finances_pesa.data as d
import econdata.ukgov_finances_pesa.db
import econdata.ukgov_finances_cra.db

class WdmmgController(BaseController):
    dbmod = econdata.ukgov_finances_pesa.db
    dbpath = os.path.join(config['db_store_path'], 'ukgov_finances_pesa.db')
    dburi = 'sqlite:///%s' % dbpath

    dbmodcra = econdata.ukgov_finances_cra.db
    dbpathcra = os.path.join(config['db_store_path'], 'ukgov_finances_cra.db')
    dburicra = 'sqlite:///%s' % dbpathcra

    def __before__(self):
        self.dbmod.Session.clear()
        self.repo = self.dbmod.Repository(self.dburi)

        self.dbmodcra.Session.clear()
        self.repocra = self.dbmodcra.Repository(self.dburicra)

    def __after__(self):
        self.dbmod.Session.remove()
        self.dbmodcra.Session.remove()

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
        td = swiss.tabular.TabularData()
        td.header = ['Year', 'Title', 'Amount']
        td.data = [ [ e.date, e.title, e.amount] for e in c.expenditures ]
        tdout = swiss.tabular.pivot(td,'Year','Title','Amount')
        # tdouttable = swiss.tabular.pivot(td,'Title','Year','Amount')

        plotctr = econ.www.controllers.plot.PlotController()
        c.html_table = genshi.XML(plotctr.get_html_table(tdout))
        c.chart_code = genshi.HTML(plotctr._get_chart_code(tdout))

        return render('wdmmg/table')

    def spend(self):
        a = d.Analyzer()
        entries, years = a.extract_simple()
        expenditure = entries['Public sector current expenditure']
        td = swiss.tabular.TabularData(
                header=['Year'],
                data=[years]
                )
        for k,v in entries.items():
            td.header.append(k)
            td.data.append(v)
        td.data = swiss.tabular.transpose(td.data)

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
        try:
            levels = int(request.params.get('levels', 2))
        except:
            levels = 2
        a = d.Analyzer()
        # data = a.extract_dept_spend_for_jit()
        data = a.department_and_function(order, levels=levels)
        c.json = data
        if order == 'department':
            c.fig_title = 'UK Government Spending by Department then Function (2008)'
        else:
            c.fig_title = 'UK Government Spending by Function then Department (2008)'
        return render('wdmmg/dept')

    def cra(self, id=None):
        q = request.params.get('q', '')
        q = q.strip()
        if q:
            Prog = self.dbmodcra.Area
            dbq = Prog.query.filter(Prog.title.ilike('%'+q+'%'))
            c.count_results = dbq.count()
            c.results = dbq.limit(200).all()
        c.q = q
        return render('wdmmg/cra')

    def _handle_series_changes(self):
        # we hack in some storage using cookies
        if not 'datasets' in session:
            session['datasets'] = []
        seriesid = request.params.get('series_id')
        change = request.params.get('change', 'add')
        if seriesid:
            if change == 'add':
                session['datasets'] = session['datasets'] + [seriesid]
            elif change == 'remove':
                print 'removing', seriesid
                if seriesid in session['datasets']:
                    session['datasets'].remove(seriesid)
            session.save()
        if 'clear' in request.params:
            session['datasets'] = []
            session.save()

    def myseries(self, id=None):
        # overloading one url to be both add and view ...
        self._handle_series_changes()
        # now do display
        # from pylons import session
        c.programmes = []
        for seriesid in session['datasets']:
            dataset_code, id = seriesid.split('---')
            if dataset_code == 'cra':
                prg = self.dbmodcra.Area.query.get(id)
                c.programmes.append(prg)

        td = swiss.tabular.TabularData()
        td.header = ['Year', 'Title', 'Amount']
        for prg in c.programmes:
            td.data += [ [ e.year, prg.title + '-' + prg.region, e.amount] for e in prg.expenditures ]
        tdout = swiss.tabular.pivot(td,'Year','Title','Amount')
        plotctr = econ.www.controllers.plot.PlotController()
        c.html_table = genshi.XML(plotctr.get_html_table(tdout))
        c.chart_code = genshi.HTML(plotctr._get_chart_code(tdout))
        return render('wdmmg/myseries')

