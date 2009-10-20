'''Use SQLAlchemy to load data into sql db and provide a pythonic interface.
'''
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Session = scoped_session(sessionmaker(
    autoflush=True, transactional=False
    ))
Base = declarative_base(mapper=Session.mapper)

class PesaTable(Base):
    __tablename__ = 'pesatable'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', Unicode(300))
    tags = Column('tags', UnicodeText)
    # store using simplejson
    footnotes = Column('footnotes', UnicodeText)

class Expenditure(Base):
    __tablename__ = 'expenditure'
    id = Column('id', Integer, primary_key=True)
    title = Column('name', Unicode(300))
    amount = Column('amount', Float)
    # maybe should be date
    date = Column('date', UnicodeText)
    tags = Column('tags', UnicodeText)
    pesatable_id = Column('pesatable_id', Integer, ForeignKey('pesatable.id'))
    pesatable = relation('PesaTable', backref='expenditures')

class Repository:
    def __init__(self, dburi):
        engine = create_engine(dburi)
        Base.metadata.bind = engine
        Session.bind = engine
        Base.metadata.create_all(bind=engine)

