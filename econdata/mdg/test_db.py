import db

dburi = 'sqlite:///:memory:'

class TestRepository:
    repo = db.Repository(dburi)

    def test_domain_model(self):
        country = db.Country(code=1, name='Argentina')
        series = db.Series(code=694, name='GDP', is_goal=True)
        value = db.Value(
            country=country,
            series=series,
            year=1990,
            value=0.5)
        db.Session.flush()
        db.Session.clear()
        vals = db.Value.query.all()
        assert len(vals) == 1
        assert vals[0].value == 0.5
        assert vals[0].country.name == 'Argentina'

