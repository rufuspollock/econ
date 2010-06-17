# development index controller
from econ.www.controllers.mdg import *
import econdata.ciafactbook.db

class HwiController(MdgController):
    dbmod = econdata.ciafactbook.db
    dbpath = os.path.join(config['db_store_path'], 'sqlite_ciafactbook.db')
    dburi = 'sqlite:///%s' % dbpath

    def create(self):
        c.series = self.dbmod.Series.query.order_by(self.dbmod.Series.name).all()
        return render('hwi/create')

    def hdi(self):
        gdp = self.dbmod.Series.query.filter_by(
                name='GDP (purchasing power parity)'
                ).first()
        ue = self.dbmod.Series.query.filter_by(
                name='Unemployment rate(%)'
                ).first()
        le = self.dbmod.Series.query.filter_by(
                name='Life expectancy at birth(years)'
                ).first()
        self.dbmod.Value.query()
        out = []
        for c in self.dbmod.Country.query.all():
            pass

    def view(self, id):
        countries = request.params.getall('countries')
        series = request.params.get('series')
        try:
            c.series = self.dbmod.Series.query.get(series)
        except:
            h.redirect_to(controller='hwi', action='index', id=None)
        c.values = self.dbmod.Value.query.filter(
                self.dbmod.Value.country_code.in_(countries)).filter_by(
                        series_code=series).all()
        c.countries = [ self.dbmod.Country.query.get(ctry) for ctry in countries ]
        td = self._cvt_values_to_tabular(c.values)

        import econ.www.controllers.plot
        plotctr = econ.www.controllers.plot.PlotController()
        c.html_table = genshi.XML(plotctr.get_html_table(td))
        c.chart_code = genshi.HTML(plotctr._get_chart_code(td))
        # return render('plot/chart', strip_whitespace=False)
        return render('mdg/view')

            
