import uuid

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
metadata = MetaData()

Session = scoped_session(sessionmaker(
    autoflush=True, transactional=True
    ))
Base = declarative_base(mapper=Session.mapper)

def make_uuid(): return unicode(uuid.uuid4())

## NOT using Account, Transaction, Tag model as yet ...
class Account(Base):
    __tablename__ = 'account'
    id = Column(UnicodeText, primary_key=True, default=make_uuid)
    title = Column(UnicodeText)
    notes = Column(UnicodeText)
    # Parent account (if any)
    # Column('parent', UnicodeText, primary_key=True, default=make_uuid)

# should have two items here (journal + transaction/posting) for proper double
# entry but do not bother for the present
class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(UnicodeText, primary_key=True, default=make_uuid)
    timestamp = Column(UnicodeText)
    timestamp_ordered = Column(DateTime)
    amount = Column(Float)
    source_id = Column(UnicodeText, ForeignKey('account.id'))
    source = relation('Account', backref='transaction',
            primaryjoin=source_id==Account.id,
            )
    dest_id = Column(UnicodeText, ForeignKey('account.id'))
    dest = relation('Account', backref='transaction_dest',
            primaryjoin=dest_id==Account.id,
            )

class Tag(Base):
    __tablename__ = 'tag'
    id = Column('id', Integer, primary_key=True)


## Alternative (simpler) domain model for CRA data
class Area(Base):
    __tablename__ = 'area'
    id = Column(UnicodeText, primary_key=True, default=make_uuid)
    title = Column(UnicodeText)
    department = Column(UnicodeText)
    subfunction = Column(UnicodeText)
    region = Column(UnicodeText)
    cap_or_cur = Column(UnicodeText)
    notes = Column(UnicodeText)

    @property
    def series_id(self):
        return 'cra---' + self.id

    @property
    def descriptor(self):
        return ' - '.join([self.title, self.region, self.department])

class Expenditure(Base):
    __tablename__ = 'expenditure'
    id = Column(UnicodeText, primary_key=True, default=make_uuid)
    year = Column(Integer)
    amount = Column(Float)
    area_id = Column(UnicodeText, ForeignKey('area.id'))
    area = relation('Area', backref='expenditures')


class Repository:
    def __init__(self, dburi):
        engine = create_engine(dburi)
        Base.metadata.bind = engine
        Session.bind = engine
        Base.metadata.create_all(bind=engine)

    def load_normed_data(self, fp):
        pass

