import os
from StringIO import StringIO

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
        c.series = db.Series.query.all()
        return render('mdg/index')

    def series(self, id):
        c.series = db.Series.query.get(id)
        c.countries = sorted(list(set(
            [x.country for x in c.series.values]
            )),
            lambda x,y: cmp(x.code, y.code)
            )
        return render('mdg/series')

    def country(self, id):
        c.country = db.Country.query.get(id)
        c.series = sorted(list(set(
            [x.series for x in c.country.values]
            )),
            lambda x,y: cmp(x.code, y.code)
            )
        return render('mdg/country')

    def _cvt_values_to_csv(self, values):
        td = econ.data.tabular.TabularData()
        td.header = ['Year', 'Country', 'Value']
        td.data = [ [v.year, v.country.name, v.value] for v in values ]
        tdout = econ.data.pivot(td, 0,1,2)
        return tdout

    def view(self, id=None):
        country = request.params.getall('country')
        series = request.params.get('series')
        c.values = db.Value.query.filter(
                db.Value.country_code.in_(country)).filter_by(
                        series_code=series).all()
        c.country = db.Country.query.get(country[0])
        c.series = db.Series.query.get(series)
        td = self._cvt_values_to_csv(c.values)
        import econ.www.controllers.plot
        fileobj = StringIO()
        econ.data.tabular.CsvWriter().write(fileobj, td)
        fileobj.seek(0)
        plotctr = econ.www.controllers.plot.PlotController()
        c.html_table = genshi.XML(plotctr.get_html_table(fileobj))
        fileobj.seek(0)
        c.chart_code = genshi.HTML(plotctr._get_chart_code(fileobj))
        # return render('plot/chart', strip_whitespace=False)
        return render('mdg/view')

    def hdi(self):
        return render('mdg/hdi')

    def create(self):
        # TODO:
        return 'Created Ok'
