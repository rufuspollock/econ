# Download and manipulate data from Millenium Development Goals Project
# http://mdgs.un.org/unsd/mdg/
import urllib
import zipfile
from StringIO import StringIO

def all_data():
    '''
    Now (2007-12) seems you can get all datasets in one big csv file.

    Note that the end result is a bit unwieldly being > 9MB
    '''
    url = 'http://mdgs.un.org/unsd/mdg/Handlers/ExportHandler.ashx?Type=Csv'
    openurl = urllib.urlopen(url)
    tfo = StringIO(openurl.read())
    zipfo = zipfile.ZipFile(tfo)
    # there is just one item in the zip archive
    name = zipfo.namelist()[0]
    out = zipfo.read(name)
    return out

def download_data(series_id, format='csv'):
    """Download a given data series.

    @format: csv, xml, xls (excel)
    """
    format = format.capitalize()
    url = 'http://mdgs.un.org/unsd/mdg/Handlers/ExportHandler.ashx' + \
            '?Type=%s&Series=%s' % (format, series_id)
    openurl = urllib.urlopen(url)
    tfo = StringIO(openurl.read())
    zipfo = zipfile.ZipFile(tfo)
    # there is just one item in the zip archive
    name = zipfo.namelist()[0]
    out = zipfo.read(name)
    return out

def parse_data_file(csv_fo):
    # TODO: leave this to parse all data.
    pass

def norm_all_data(csv_fo, out_fo):
    '''Normalizes the standard csv file to have year/value information as
    columns rather than going across horizontally.

    TODO:? do we delete footnote rows at end of file or ...?
    '''
    import csv
    reader = csv.reader(csv_fo)
    writer = csv.writer(out_fo)
    for row in reader:
        # hit a blank line means footnotes are to begin so halt ...
        if len(row) == 0:
            break
        # TODO: finish this off (and write test)

def parse_all_data(csv_fo):
    '''Parses the csv file containing all data.
    
    TODO: normalize data.

    @csv_fo: the csv fileobject to parse.
    @return: a tuple (countries, series, rows, footnotes) where:
        countries: a dictionary of country code (key) country name (value)
            pairs
        series: a dictionary keyed by series code and values consisting of
            tuple series title and a boolean indicating whether a MDG or not.
        rows: a list of rows each row being an object with country_code,
            series_code and list of values where each value is an object with
            attributes value, type and footnotes (list).
        footnotes: dictionary keyed by id with value the footnote text.
    '''
    import csv
    reader = csv.reader(csv_fo)
    matrix = []
    footnote_matrix = []
    # headings in first row
    headings = reader.next()
    footnotes_started = False
    count = -1
    for line in reader:
        count += 1
        if footnotes_started:
            footnote_matrix.append(line)
        else:
            matrix.append(line)
        # blank line with nothing in separates footnotes
        if len(line) == 0:
            footnotes_started = True
    # throw out blank and footnote heading line
    matrix = matrix[:-1]
    type_info = footnote_matrix[-9:-1]
    # TODO: print type_info
    footnote_matrix = footnote_matrix[1:-10]
    countries = {}
    for row in matrix:
        code = row[0]
        name = row[1]
        countries[code] = name
    footnotes = {}
    for row in footnote_matrix:
        footnotes[row[0]] = row[1]
    series = {}
    for row in matrix:
        code = row[2]
        name = row[4]
        is_mdg = True
        if row[3] == 'N': is_mdg = False
        series[code] = (name, is_mdg)

    class Value:
        def __init__(self, value, type, footnotes):
            self.__dict__.update(locals())
        
    class Row:
        def __init__(self, country_code, series_code, values):
            self.__dict__.update(locals())

    def parse_values(vlist):
        values = {}
        # groups of 3
        for ii in range(len(vlist)/3):
            offset = 3 * ii
            value_str = vlist[offset].strip()
            if value_str: 
                value = float(value_str)
            else:
                value = None
            # can have multiple footnotes e.g. '25;90'
            # fn_id_str = vlist[offset+1].strip()
            # if fn_id_str:
            #     fn_id = int(fn_id_str)
            # else:
            #     fn_id = None
            footnotes = vlist[offset+1]
            type = vlist[offset+2]
            values[1990 + ii] = Value(value, type, footnotes)
        return values

    rows = []
    for row in matrix:
        ccode = row[0]
        scode = row[2]
        row = row[5:]
        values =  parse_values(row)
        rows.append(Row(ccode, scode, values))

    return countries, series, rows, footnotes

class SqlalchemyWrapper:
    '''Use SQLAlchemy to load data into sql db and provide a pythonic
    interface.

    # TODO: complete this.
    '''

    def __init__(self):
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///:memory:', echo=True)

    def map(self):
        class Country:
            name = String()
            code = Int()

        class Series: # not always a goal ...
            code = Int()
            name = String()
            is_goal = Boolean()

        class Value:
            value = Blah()
            type = String()
            footnote = ForeignKey() 

    class Footnote:
        id = None
        text = None


class MdgMetadata(object):

    def __init__(self):
        metadata_csv = self._load_cached_metadata()
        self.series = self._parse_metadata_csv(metadata_csv)

    def _load_cached_metadata(self):
        import pkg_resources
        # TODO: change this to local directory (not using econ.mdg any more)
        metafo = pkg_resources.resource_stream('econ.mdg', 'mdg_metadata.txt')
        return metafo

    def _parse_metadata_csv(self, fileobj):
        outdict = {}
        import csv
        reader = csv.reader(fileobj)
        for row in reader:
            series_id = int(row[0])
            title = row[1]
            outdict[series_id] = title
        return outdict

    def _download_metadata():
        # does *NOT* work because of nasty javascript
        # probably need to use selenium
        from mechanize import Browser
        br = Browser()
        br.addheaders = [ ('User-agent', 'Firefox') ]
        br.set_handle_robots(False)
        br.open('http://mdgs.un.org/unsd/mdg/Metadata.aspx')
        br.follow_link(text='Flat View')
        assert br.viewing_html()
        out = br.response().read()
        # TODO: extract option list and then clean up
        return out

def do_everything():
    out = all_data()
    ff = file('all_in_one.csv', 'w')
    ff.write(out)
    ff.close()

# ---------------------------------------------------------
# TESTS

def test_parse():
    ff = file('all_in_one.csv')
    countries, series, rows, footnotes = parse_all_data(ff)
    ff.close()
    assert len(countries) == 231
    assert len(series) == 128
    lr = len(rows)
    assert lr == 29568
    row = rows[27649]
    uk_ppp = row.values[1990].value
    print row.series_code
    print row.country_code
    print uk_ppp
    assert uk_ppp == 0.5491460491
                
if __name__ == '__main__':
    # out = download_data(580, 'csv')
    # print out
    pass
