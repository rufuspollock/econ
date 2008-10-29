'''Download and manipulate data from Millenium Development Goals Project

http://mdgs.un.org/unsd/mdg/
'''
import urllib
import zipfile
from StringIO import StringIO
import csv

original_fn = 'data_original.csv'

def download_all_data():
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

    fo = file(original_fn, 'w')
    fo.write(out)
    fo.close()

def download_single_series(series_id, format='csv'):
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

class DataParser(object):
    def __init__(self):
        pass
        # self.fileobj = fileobj

    def norm_all_data(self, csv_fo, out_fo, footnotes_fo):
        '''Normalizes the standard csv file to have year/value information as
        columns rather than going across horizontally.

        @csv_fo: the csv fileobject to parse.
        @out_fo: fileobject to write to.
        @footnotes_fo: fileobject in which to store footnotes.
        '''
        reader = csv.reader(csv_fo)
        writer = csv.writer(out_fo)
        footnote_matrix = []
        # headings in first row
        headings = reader.next()
        headings = headings[:6] + ['Year', 'Value', 'Footnotes', 'Type']
        writer.writerow(headings)

        footnotes_started = False
        count = -1
        for line in reader:
            count += 1
            # blank line with nothing in separates footnotes
            if len(line) == 0 or footnotes_started:
                footnotes_started = True
                footnote_matrix.append(line)
            else:
                try:
                    newrows = self.norm_row(line)
                    writer.writerows(newrows)
                except:
                    print count
                    print line
        footnote_matrix = footnote_matrix[1:-10]
        # discard type info as now in metadata.txt
        # type_info = footnote_matrix[-9:-1]
        footnote_matrix = footnote_matrix[1:-10]
        fnwriter = csv.writer(footnotes_fo)
        fnwriter.writerows(footnote_matrix)

    def norm_row(self, row):
        '''Normalize rows.

        Take in data in form 

        ['CountryCode', 'Country', 'SeriesCode', 'MDG', 'Series',
            '1990', 'Footnotes', 'Type', '1991', 'Footnotes', 'Type',
            ...

        And return in form:

        ['CountryCode', 'Country', 'SeriesCode', 'MDG', 'Series', 'Year', 'Value',
        'Footnotes', 'Type' ]

        NB: if no value that year is omitted.
        '''
        results = []
        start_year = 1990
        end_year = 2008
        for year in range(start_year, end_year):
            newrow = row[:5]
            newrow.append(year)
            start = 5 + 3 * (year-start_year)
            newrow += row[start:start+3]
            value = newrow[6].strip()
            if value:
                results.append(newrow)
        return results

    def parse_all_data(self, csv_fo):
        '''Parses the original csv file containing all data.
        
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
        type_info = footnote_matrix[-9:-1]
        # TODO: print type_info
        footnotes = self.parse_footnotes(footnote_matrix)
        countries, series, rows = self.parse_data_matrix(matrix)

        return countries, series, rows, footnotes

    def parse_footnotes(self, footnote_matrix):
        footnote_matrix = footnote_matrix[1:-10]
        footnotes = {}
        for row in footnote_matrix:
            footnotes[row[0]] = row[1]
        return footnotes

    def parse_data_matrix(self, matrix):
        # throw out blank and footnote heading line
        matrix = matrix[:-1]
        countries = {}
        for row in matrix:
            code = row[0]
            name = row[1]
            countries[code] = name
        series = {}
        for row in matrix:
            code = row[2]
            name = row[4]
            is_mdg = True
            if row[3] == 'N': is_mdg = False
            series[code] = (name, is_mdg)

        class Row:
            def __init__(self, country_code, series_code, values):
                self.__dict__.update(locals())

        rows = []
        for row in matrix:
            ccode = row[0]
            scode = row[2]
            row = row[5:]
            values =  self.parse_values(row)
            rows.append(Row(ccode, scode, values))
        return countries, series, rows


    def parse_values(self, vlist):
        class Value:
            def __init__(self, value, type, footnotes):
                self.__dict__.update(locals())
            
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


class MdgMetadata(object):
    '''TODO.'''

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
                

dburi = 'sqlite:///%s' % 'sqlite_mdg.db'
def load_normed_data_into_db():
    fn = 'data.csv'
    import db
    repo = db.Repository(dburi)
    repo.load_normed_data(fn)

def norm_data():
    parser = DataParser()
    fo = file(original_fn)
    fo2 = file('data.csv', 'w')
    fo3 = file('footnotes.csv', 'w')
    parser.norm_all_data(fo, fo2, fo3)

def main():
    download_all_data()
    norm_data()

if __name__ == '__main__':
    # main()
    load_normed_data_into_db()


