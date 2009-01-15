'''Use SQLAlchemy to load data into sql db and provide a pythonic interface.
'''
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Session = scoped_session(sessionmaker(
    autoflush=True, transactional=False,
    ))
Base = declarative_base(mapper=Session.mapper)

class Country(Base):
    __tablename__ = 'country'
    code = Column('code', Integer, primary_key=True)
    name = Column('name', UnicodeText)

class Series(Base): # not always a goal ...
    __tablename__ = 'series'
    code = Column('code', Integer(), primary_key=True)
    name = Column('name', UnicodeText)

class Value(Base):
    __tablename__ = 'value'
    id = Column('id', Integer, primary_key=True)
    year = Column('year', Integer)
    value = Column('value', Float)
    country_code = Column('country_code', Integer, ForeignKey('country.code'))
    country = relation('Country', backref='values')
    series_code = Column('series_code', Integer, ForeignKey('series.code'))
    series = relation('Series', backref='values')


class Repository:
    def __init__(self, dburi):
        engine = create_engine(dburi)
        Base.metadata.bind = engine
        Session.bind = engine
        Base.metadata.create_all(bind=engine)

'''Use SQLAlchemy to load data into sql db and provide a pythonic interface.
'''
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Session = scoped_session(sessionmaker(
    autoflush=True, transactional=False,
    ))
Base = declarative_base(mapper=Session.mapper)

class Country(Base):
    __tablename__ = 'country'
    code = Column('code', Integer, primary_key=True)
    name = Column('name', UnicodeText)

class Series(Base): # not always a goal ...
    __tablename__ = 'series'
    code = Column('code', Integer(), primary_key=True)
    name = Column('name', UnicodeText)

class Value(Base):
    __tablename__ = 'value'
    id = Column('id', Integer, primary_key=True)
    year = Column('year', Integer)
    value = Column('value', Float)
    country_code = Column('country_code', Integer, ForeignKey('country.code'))
    country = relation('Country', backref='values')
    series_code = Column('series_code', Integer, ForeignKey('series.code'))
    series = relation('Series', backref='values')


class Repository:
    def __init__(self, dburi):
        engine = create_engine(dburi)
        Base.metadata.bind = engine
        Session.bind = engine
        Base.metadata.create_all(bind=engine)

