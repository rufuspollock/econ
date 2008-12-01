'''Use SQLAlchemy to load data into sql db and provide a pythonic interface.
'''
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Session = scoped_session(sessionmaker(
    autoflush=True, transactional=False
    ))
Base = declarative_base(mapper=Session.mapper)

class Country(Base):
    __tablename__ = 'country'
    code = Column('code', Integer, primary_key=True)
    name = Column('name', String(300))

class Series(Base): # not always a goal ...
    __tablename__ = 'series'
    code = Column('code', Integer(), primary_key=True)
    name = Column('name', Text())
    is_goal = Column('is_goal', Boolean())

class Value(Base):
    __tablename__ = 'value'
    id = Column('id', Integer, primary_key=True)
    year = Column('year', Integer)
    value = Column('value', Float)
    type = Column('type', String(1))
    country_code = Column('country_code', Integer, ForeignKey('country.code'))
    country = relation('Country', backref='values')
    series_code = Column('series_code', Integer, ForeignKey('series.code'))
    series = relation('Series', backref='values')
    footnotes = Column('footnotes', Text)

#class Footnote:
#    id = None
#    text = None


class Repository:
    def __init__(self, dburi):
        engine = create_engine(dburi)
        Base.metadata.bind = engine
        Session.bind = engine
        Base.metadata.create_all(bind=engine)

    def load_normed_data(self, fp):
        import csv
        reader = csv.DictReader(open(fp))
        countries = {}
        series = {}
        count = -1
        for row in reader:
            count += 1
            if count % 1000 == 0:
                print count
            value = Value()
            ccode = int(row['CountryCode'])
            scode = int(row['SeriesCode'])
            sname = row['Series']
            countries[ccode] = row['Country']
            is_mdg = row['MDG'] == 'Y'
            series[scode] = (sname, is_mdg)
            # define fk values directly so not a problem we do not define
            # country/series objects until later
            value.country_code = ccode
            value.series_code = scode
            value.value = float(row['Value'])
            value.footnoteos = row['Footnotes']
            value.type = row['Type']
            value.year = int(row['Year'])
        for k,v in countries.items():
            Country(code=k, name=v)
        for k,v in series.items():
            Series(code=k, name=v[0], is_goal=v[1])
        # can only flush until here as need Country and Series objects set up
        # for fks
        Session.flush()

