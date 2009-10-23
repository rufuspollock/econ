import db

dburi = 'sqlite:///:memory:'
repo = db.Repository(dburi)

class TestDb:
    def test_all(self):
        acc = db.Account(title=u'my account')
        acc2 = db.Account(title=u'your account')
        txn = db.Transaction(amount=10.0,
                source=acc)
            # dest=acc2
        db.Session.commit()

    def test_expenditure(self):
        ar = db.Area(title=u'xyz')
        exp = db.Expenditure(amount=10.0, area=ar)
        db.Session.commit()

