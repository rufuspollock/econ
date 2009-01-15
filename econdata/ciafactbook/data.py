'''Get statistical info from CIA World Fact Book.

    %prog {year}

Download factbook for year {year} and extract info into an sqlite db and a
data.csv in this directory.

NB: info extracted is that in rank order tables.
'''
baseurl = \
'https://www.cia.gov/library/publications/download/download-%s/factbook.zip'

import econ.data
import zipfile
class Extractor:
    def __init__(self, year):
        self.year = int(year)
        self.url = baseurl % self.year
        # have to name cache different as factbook is named the same
        self.retriever = econ.data.Retriever('cache_%s' % year)

    def _print(self, msg, force=False):
        print(msg)

    def execute(self):
        self.download()
        ros = self.rankorders()
        normed_tdata = econ.data.TabularData(
                header=['Series', 'Country', 'Value', 'Year']
                )
        for ro in ros:
            self._print('Processing %s' % ro)
            tdata = self.parse_rank_file(ro)
            # Series, Country, Value, Year
            series = unicode(tdata.header[1])
            normed = [ [series] + row for row in tdata.data]
            normed_tdata.data += normed
            self.load_into_db(normed)
        writer = econ.data.CsvWriter()
        writer.write(open('data.csv', 'w'), normed_tdata)

    def download(self):
        path = self.retriever.retrieve(self.url)

    def rankorders(self):
        rankorder_dir = 'factbook/rankorder/'
        path = self.retriever.filepath(self.url)
        zf = zipfile.ZipFile(path)
        rankorders = [ name for name in zf.namelist() if \
                name.startswith(rankorder_dir) and name.endswith('.txt') ]
        return rankorders
    
    def parse_rank_file(self, path):
        '''Parse rank file into something useful.

        Files are tab delimited.
        
          * First row is info about tab-delimited stuff
          * Last row gives updated date

        @return: TabularData object with cols Country, Series Values, Year
        '''
        zfpath = self.retriever.filepath(self.url)
        zf = zipfile.ZipFile(zfpath)
        content = zf.read(path)
        rows = content.split('\n')
        tdata = econ.data.TabularData()
        # Rank, Country, Series Name, Date of Information
        tdata.header = rows[1].split('\t')[1:3] + ['Year']
        tdata.header = [ x.strip() for x in tdata.header ]
        rows = rows[2:-3]
        for row in rows:
            cols = row.split('\t')
            # note est year is usually self.year - 1
            # we discard consolidated groupings such as World and EU
            country = cols[1].strip()
            if country not in ['World'] and 'Ocean' not in country:
                val = cols[2].strip()
                if val.startswith('$'): val = val[1:].strip()
                val = econ.data.floatify(val)
                tdata.data.append([
                   unicode(country), val, self.year])
        return tdata

    def load_into_db(self, normed_data):
        dburi = 'sqlite:///%s' % 'sqlite_ciafactbook.db'
        import db
        repo = db.Repository(dburi)
        # Series, Country, Value, Year
        countries = {}
        seriess = {}
        def goc(thedict, thekey, thetype):
            if not thekey in thedict:
                existing = thetype.query.filter_by(name=thekey).first()
                if not existing:
                    thedict[thekey] = thetype(name=thekey)
                else:
                    thedict[thekey] = existing
            return thedict[thekey]

        for row in normed_data:
            series = goc(seriess, row[0], db.Series)
            country = goc(countries, row[1], db.Country)
            val = db.Value(
                series=series,
                country=country,
                value=row[2],
                year=row[3],
                )
        db.Session.flush()

class TestExtractor:

    @classmethod
    def setup_class(self):
        self.e = Extractor(2007)
        self.e.download()
        self.rankorders = self.e.rankorders()

    def test_rankorders(self):
        rankorders = self.rankorders
        assert len(rankorders) == 50, len(rankorders)
    
    def test_parse_rank(self):
        # first is 2001 and is GDP
        out = self.e.parse_rank_file(self.rankorders[0])
        assert out.header[0] == 'Country', out.header
        assert len(out.data) == 228, len(out.data)
        row = out.data[0]
        assert len(row) == 3
        assert row[1] == 13080000000000.0, row
        assert row[2] == 2007

import optparse
import sys
if __name__ == '__main__':
    parser = optparse.OptionParser(__doc__)
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)
    e = Extractor(args[0])
    e.execute()

'''Get statistical info from CIA World Fact Book.

    %prog {year}

Download factbook for year {year} and extract info into an sqlite db and a
data.csv in this directory.

NB: info extracted is that in rank order tables.
'''
baseurl = \
'https://www.cia.gov/library/publications/download/download-%s/factbook.zip'

import econ.data
import zipfile
class Extractor:
    def __init__(self, year):
        self.year = int(year)
        self.url = baseurl % self.year
        # have to name cache different as factbook is named the same
        self.retriever = econ.data.Retriever('cache_%s' % year)

    def _print(self, msg, force=False):
        print(msg)

    def execute(self):
        self.download()
        ros = self.rankorders()
        normed_tdata = econ.data.TabularData(
                header=['Series', 'Country', 'Value', 'Year']
                )
        for ro in ros:
            self._print('Processing %s' % ro)
            tdata = self.parse_rank_file(ro)
            # Series, Country, Value, Year
            series = unicode(tdata.header[1])
            normed = [ [series] + row for row in tdata.data]
            normed_tdata.data += normed
            self.load_into_db(normed)
        writer = econ.data.CsvWriter()
        writer.write(open('data.csv', 'w'), normed_tdata)

    def download(self):
        path = self.retriever.retrieve(self.url)

    def rankorders(self):
        rankorder_dir = 'factbook/rankorder/'
        path = self.retriever.filepath(self.url)
        zf = zipfile.ZipFile(path)
        rankorders = [ name for name in zf.namelist() if \
                name.startswith(rankorder_dir) and name.endswith('.txt') ]
        return rankorders
    
    def parse_rank_file(self, path):
        '''Parse rank file into something useful.

        Files are tab delimited.
        
          * First row is info about tab-delimited stuff
          * Last row gives updated date

        @return: TabularData object with cols Country, Series Values, Year
        '''
        zfpath = self.retriever.filepath(self.url)
        zf = zipfile.ZipFile(zfpath)
        content = zf.read(path)
        rows = content.split('\n')
        tdata = econ.data.TabularData()
        # Rank, Country, Series Name, Date of Information
        tdata.header = rows[1].split('\t')[1:3] + ['Year']
        tdata.header = [ x.strip() for x in tdata.header ]
        rows = rows[2:-3]
        for row in rows:
            cols = row.split('\t')
            # note est year is usually self.year - 1
            # we discard consolidated groupings such as World and EU
            country = cols[1].strip()
            if country not in ['World'] and 'Ocean' not in country:
                val = cols[2].strip()
                if val.startswith('$'): val = val[1:].strip()
                val = econ.data.floatify(val)
                tdata.data.append([
                   unicode(country), val, self.year])
        return tdata

    def load_into_db(self, normed_data):
        dburi = 'sqlite:///%s' % 'sqlite_ciafactbook.db'
        import db
        repo = db.Repository(dburi)
        # Series, Country, Value, Year
        countries = {}
        seriess = {}
        def goc(thedict, thekey, thetype):
            if not thekey in thedict:
                existing = thetype.query.filter_by(name=thekey).first()
                if not existing:
                    thedict[thekey] = thetype(name=thekey)
                else:
                    thedict[thekey] = existing
            return thedict[thekey]

        for row in normed_data:
            series = goc(seriess, row[0], db.Series)
            country = goc(countries, row[1], db.Country)
            val = db.Value(
                series=series,
                country=country,
                value=row[2],
                year=row[3],
                )
        db.Session.flush()

class TestExtractor:

    @classmethod
    def setup_class(self):
        self.e = Extractor(2007)
        self.e.download()
        self.rankorders = self.e.rankorders()

    def test_rankorders(self):
        rankorders = self.rankorders
        assert len(rankorders) == 50, len(rankorders)
    
    def test_parse_rank(self):
        # first is 2001 and is GDP
        out = self.e.parse_rank_file(self.rankorders[0])
        assert out.header[0] == 'Country', out.header
        assert len(out.data) == 228, len(out.data)
        row = out.data[0]
        assert len(row) == 3
        assert row[1] == 13080000000000.0, row
        assert row[2] == 2007

import optparse
import sys
if __name__ == '__main__':
    parser = optparse.OptionParser(__doc__)
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)
    e = Extractor(args[0])
    e.execute()

