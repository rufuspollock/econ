import os

import genshi

from econ.www.lib.base import *
import econ.data.tabular
import econdata.mdg.db as db

dbpath = os.path.join(config['db_store_path'], 'mdg.db')
dburi = 'sqlite:///%s' % dbpath

class MdgController(BaseController):

    def __before__(self):
        db.Session.clear()
        self.repo = db.Repository(dburi)

    def __after__(self):
        db.Session.remove()

    def index(self):
        c.num_series = db.Series.query.count()
        c.num_countries = db.Country.query.count()
        return render('mdg/index')

    def series(self, id=None):
        if id is None:
            return self.series_list()
        c.series = db.Series.query.get(id)
        if not c.series:
            abort(404)
        c.countries = sorted(list(set(
            [x.country for x in c.series.values]
            )),
            lambda x,y: cmp(x.code, y.code)
            )
        return render('mdg/series')

    def series_list(self):
            c.items = db.Series.query.all()
            return render('mdg/series_list')

    def country(self, id):
        if id is None:
            return self.country_list()
        c.country = db.Country.query.get(id)
        if not c.country:
            abort(404)
        c.series = sorted(list(set(
            [x.series for x in c.country.values]
            )),
            lambda x,y: cmp(x.code, y.code)
            )
        return render('mdg/country')

    def country_list(self):
            c.items = db.Country.query.all()
            return render('mdg/country_list')

    def _cvt_values_to_tabular(self, values):
        td = econ.data.tabular.TabularData()
        td.header = ['Year', 'Country', 'Value']
        td.data = [ [v.year, v.country.name, v.value] for v in values ]
        tdout = econ.data.pivot(td,0,1,2)
        return tdout

    def view(self, id=None):
        countries = request.params.getall('countries')
        series = request.params.get('series')
        c.values = db.Value.query.filter(
                db.Value.country_code.in_(countries)).filter_by(
                        series_code=series).all()
        c.countries = [ db.Country.query.get(ctry) for ctry in countries ]
        c.series = db.Series.query.get(series)
        td = self._cvt_values_to_tabular(c.values)

        import econ.www.controllers.plot
        plotctr = econ.www.controllers.plot.PlotController()
        c.html_table = genshi.XML(plotctr.get_html_table(td))
        c.chart_code = genshi.HTML(plotctr._get_chart_code(td))
        # return render('plot/chart', strip_whitespace=False)
        return render('mdg/view')

    def hdi(self):
        return render('mdg/hdi')

    def create(self):
        # TODO:
        return 'Created Ok'
