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

    def view(self, id):
        # TODO: finish off
        gdp = self.dbmod.Series.query.filter_by(
                name='GDP (purchasing power parity)'
                ).first()
        ue = self.dbmod.Series.query.filter_by(
                name='Unemployment rate(%)'
                ).first()
        le = self.dbmod.Series.query.filter_by(
                name='Life expectancy at birth(years)'
                ).first()
        self.dbmod.Values.query()
        out = []
        for c in self.dbmod.Country.query.all():
            pass
            
